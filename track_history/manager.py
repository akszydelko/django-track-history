from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager
from django.db.models.loading import get_model
from django.utils.encoding import force_text
from django.utils.functional import SimpleLazyObject

from .query import SnapshotQuerySet
from .utils import has_int_pk


# Import model in a different way, because of circular imports
TrackHistoryRecord = SimpleLazyObject(lambda: get_model(__package__, 'TrackHistoryRecord'))


class TrackHistoryDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            return TrackHistoryManager(self.model)
        return TrackHistoryManager(self.model, instance)


class TrackHistoryManager(Manager):
    def __init__(self, model, instance=None):
        super(TrackHistoryManager, self).__init__()
        self.model = model
        self.instance = instance

    def get_class_content_type(self):
        return ContentType.objects.get_for_model(self.model)

    def get_queryset(self):
        defer = []
        filters = {
            'content_type': self.get_class_content_type()
        }

        if self.instance:
            if has_int_pk(self.model):
                defer.append('object_id')
                filters['object_id_int'] = int(self.instance.pk)
            else:
                defer.append('object_id_int')
                filters['object_id'] = force_text(self.instance.pk)

        return TrackHistoryRecord.objects.defer(*defer).filter(**filters)

    # Dates
    def after_date(self, date):
        return self.in_dates(from_date=date)

    def before_date(self, date):
        return self.in_dates(to_date=date)

    def in_dates(self, from_date=None, to_date=None):
        qs = self.get_queryset()

        if from_date:
            qs = qs.filter(date_created__gte=from_date)

        if to_date:
            qs = qs.filter(date_created__lte=to_date)

        return qs

    # Fields
    def get_field_history(self, field_name):
        return self.get_queryset().filter(changes__has=field_name)


class CreateAndReadOnlyManager(Manager):
    def get_or_create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError


class TrackHistorySnapshotManager(CreateAndReadOnlyManager):
    def __init__(self, *args, **kwargs):
        super(TrackHistorySnapshotManager, self).__init__(*args, **kwargs)
        self._queryset_class = SnapshotQuerySet

    def bulk_create(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def create_snapshot_for_model(self, **kwargs):
        return self.get_queryset().create_snapshot_for_model(**kwargs)
