from __future__ import unicode_literals

from operator import attrgetter

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import BaseManager
from django.utils.encoding import force_text
from django.utils.functional import SimpleLazyObject

from .query import TrackHistorySnapshotQuerySet, DateQuerySet
from .utils import has_int_pk, ContributorList

# Import model in a different way, because of circular imports
TrackHistoryRecord = SimpleLazyObject(lambda: apps.get_model(__package__, 'TrackHistoryRecord'))


class TrackHistorySnapshotManager(BaseManager.from_queryset(TrackHistorySnapshotQuerySet)):
    pass


class TrackHistoryRecordManager(BaseManager.from_queryset(DateQuerySet)):
    pass


class TrackHistoryManager(BaseManager.from_queryset(DateQuerySet)):
    def __init__(self, model, instance=None):
        super(TrackHistoryManager, self).__init__()
        self.model = model
        self.instance = instance

    def get_class_content_type(self):
        return ContentType.objects.get_for_model(self.model)

    def get_queryset(self):
        filters = {
            'content_type': self.get_class_content_type()
        }

        if self.instance:
            if has_int_pk(self.model):
                filters['object_id_int'] = int(self.instance.pk)
            else:
                filters['object_id'] = force_text(self.instance.pk)

        return TrackHistoryRecord.objects.filter(**filters)

    # Fields
    def get_field_history(self, field_name):
        return self.get_queryset().filter(changes__has_key=field_name)

    # Editors
    def get_editors(self, user_query_only=()):
        if isinstance(user_query_only, (list, tuple)):
            user_query_only = ['user__' + x for x in user_query_only]

        # We can not distinct users and order by date, so we will distinct users in the db query and order by date
        # by ourselves, which should be faster when model will have many history records.
        qs = sorted(self.get_queryset().only('user', 'date_created', 'record_type', *user_query_only)
                    .select_related('user').distinct('user_id').order_by('user_id', 'record_type'),
                    key=attrgetter('date_created'))

        editors = []
        creator = None
        for history_record in qs:
            if history_record.record_type == TrackHistoryRecord.RECORD_TYPES.created:
                creator = history_record.user
            editors.append(history_record.user)

        return ContributorList(creator=creator, editors=filter(lambda x: x, editors))

    def get_creator(self, user_query_only=()):
        if not self.instance:
            return None

        if isinstance(user_query_only, (list, tuple)):
            user_query_only = ['user__' + x for x in user_query_only]

        thr = self.get_queryset().only('user', *user_query_only).filter(
            record_type=TrackHistoryRecord.RECORD_TYPES.created).select_related('user').order_by('date_created').first()

        return thr.user if thr else None


class TrackHistoryDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            return TrackHistoryManager(self.model)
        return TrackHistoryManager(self.model, instance)
