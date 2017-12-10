from __future__ import unicode_literals
from functools import partial

from .handlers import store_initial, action_receiver, TrackHistoryModelWrapper
from django.db.models.signals import post_init, post_save, pre_delete
from .manager import TrackHistoryDescriptor
from .settings import TH_DEFAULT_EXCLUDE_FIELDS


def track_changes(model=None, fields=(), exclude=()):
    if fields and exclude:
        raise AttributeError('Attributes fields and exclude can not be specified together. Use only one of them.')

    if model is None:
        return partial(track_changes, fields=fields, exclude=exclude)

    # Remove possible duplications
    attrs = {
        '_th_fields': tuple(set(fields)),
        '_th_exclude': tuple(set(exclude + TH_DEFAULT_EXCLUDE_FIELDS))
    }

    # Connect to signals
    post_init.connect(partial(store_initial, **attrs), sender=model, weak=False,
                      dispatch_uid='django-track-history-{}'.format(model.__name__))

    post_save.connect(action_receiver, sender=model, weak=False,
                      dispatch_uid='django-track-history-{}'.format(model.__name__))

    pre_delete.connect(action_receiver, sender=model, weak=False,
                      dispatch_uid='django-track-history-{}'.format(model.__name__))

    # Hack model to inherent from TrackHistoryModelWrapper
    model.__bases__ = (TrackHistoryModelWrapper,) + model.__bases__

    # Add query manager
    descriptor = TrackHistoryDescriptor(model)
    setattr(model, 'history', descriptor)

    return model


__all__ = [
    'track_changes'
]
