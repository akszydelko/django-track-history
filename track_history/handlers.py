from __future__ import unicode_literals

from django.db import models, transaction

from .signals import th_post_init_deferred, th_post_save_deferred
from .tracker import TrackHelper


def store_initial(sender, instance, **kwargs):
    # Assign the helper instance
    setattr(instance, '_th', TrackHelper(tracked_instance=instance,
                                         fields=kwargs.get('_th_fields'), exclude=kwargs.get('_th_exclude')))


def action_receiver(sender, instance, signal, **kwargs):
    TrackHelper.signal_receiver(instance._th, instance, signal, **kwargs)


class DeferredSignalWrapper(models.Model):
    def __init__(self, *args, **kwargs):
        super(DeferredSignalWrapper, self).__init__(*args, **kwargs)
        if self._deferred:
            th_post_init_deferred.send(sender=self._meta.concrete_model, instance=self)

    def save_base(self, *args, **kwargs):
        super(DeferredSignalWrapper, self).save_base(*args, **kwargs)
        if self._deferred:
            th_post_save_deferred.send(sender=self._meta.concrete_model, instance=self, created=False,
                                       update_fields=kwargs.get('update_fields', None), using=kwargs.get('using', None))

    def save(self, *args, **kwargs):
        # Prevent any changes if model or one of history model will not save properly
        with transaction.atomic(using=kwargs.get('using', None)):
            try:
                super(DeferredSignalWrapper, self).save(*args, **kwargs)
            except:
                transaction.rollback(using=kwargs.get('using', None))
                raise

    class Meta:
        abstract = True
