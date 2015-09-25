from django.db.models.deletion import Collector

from .signals import th_pre_delete_deferred


class CustomDeletionCollector(Collector):
    def delete(self):
        # send pre_delete signals for deferred objects
        for model, obj in self.instances_with_model():
            if not model._meta.auto_created and model._deferred:
                th_pre_delete_deferred.send(sender=model._meta.concrete_model, instance=obj, using=self.using)

        super(CustomDeletionCollector, self).delete()
