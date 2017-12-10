from __future__ import unicode_literals

from django.db import models, transaction

from .tracker import TrackHelper


def store_initial(sender, instance, **kwargs):
    # Assign the helper instance
    setattr(instance, '_th', TrackHelper(tracked_instance=instance,
                                         fields=kwargs.get('_th_fields'), exclude=kwargs.get('_th_exclude')))


def action_receiver(sender, instance, signal, **kwargs):
    TrackHelper.signal_receiver(instance._th, instance, signal, **kwargs)


class TrackHistoryModelWrapper(models.Model):
    def save(self, *args, **kwargs):
        # Prevent any changes if model or one of history model will not save properly
        with transaction.atomic(using=kwargs.get('using', None)):
            super(TrackHistoryModelWrapper, self).save(*args, **kwargs)

    class Meta:
        abstract = True
