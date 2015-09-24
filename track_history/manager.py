from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_text

from track_history.models import HistoryTrackRecord, has_int_pk


class TrackHistoryDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            return TrackHistoryManager(self.model)
        return TrackHistoryManager(self.model, instance)


class TrackHistoryManager(models.Manager):
    def __init__(self, model, instance=None):
        super(TrackHistoryManager, self).__init__()
        self.model = model
        self.instance = instance

    def get_class_content_type(self):
        return ContentType.objects.get_for_model(self.model)

    def get_queryset(self):
        defer = ['history_data']
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

        return HistoryTrackRecord.objects.defer(*defer).filter(**filters)

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

