from __future__ import unicode_literals
from functools import partial

from .handlers import store_initial, action_receiver, DeferredSignalWrapper
from .signals import init_signals, save_signals, delete_signals
from .manager import TrackHistoryDescriptor


def track(model=None, fields=(), exclude=()):
    if fields and exclude:
        raise AttributeError("Attributes fields and exclude can not be specified together. Use only one of them.")

    if model is None:
        return partial(track, fields=fields, exclude=exclude)

    # Remove possible duplications
    attrs = {
        '_th_fields': tuple(set(fields)),
        '_th_exclude': tuple(set(exclude))
    }

    # Connect to signals
    for signal in init_signals:
        signal.connect(partial(store_initial, **attrs), sender=model, weak=False,
                       dispatch_uid='django-track-history-%s' % model.__name__)

    for signal in save_signals + delete_signals:
        signal.connect(action_receiver, sender=model, weak=False,
                       dispatch_uid='django-track-history-%s' % model.__name__)

    # Hack model to inherent from DeferredSignalWrapper
    model.__bases__ = (DeferredSignalWrapper,) + model.__bases__

    # Add query manager
    descriptor = TrackHistoryDescriptor(model)
    setattr(model, 'history', descriptor)

    return model


__all__ = [
    'track'
]
