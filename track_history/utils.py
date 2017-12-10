import importlib

from django.conf import settings
from django.db import models


class ContributorList(list):
    def __init__(self, creator, editors):
        super(ContributorList, self).__init__(editors)
        self.creator = creator


def has_int_pk(model):
    """Tests whether the given model has an integer primary key."""
    pk = model._meta.pk
    return (
        (
            isinstance(pk, (models.IntegerField, models.AutoField)) and
            not isinstance(pk, models.BigIntegerField)
        ) or (
            isinstance(pk, models.ForeignKey) and has_int_pk(pk.rel.to)
        )
    )


def get_track_history_record_model():
    model_path = getattr(settings, 'TH_RECORD_MODEL', 'track_history.models.TrackHistoryRecord')
    module, model_class = model_path.rsplit('.', 1)
    return getattr(importlib.import_module(module), model_class)
