from __future__ import unicode_literals
from django.conf import settings

try:
    from safedelete.signals import pre_softdelete, post_undelete
    from safedelete.models import SafeDeleteModel
    DJANGO_SAFEDELETE_INSTALLED = True
except ImportError:
    # safedelete is not installed, we don't check for its signals
    pre_softdelete = None
    post_undelete = None
    SafeDeleteModel = None
    DJANGO_SAFEDELETE_INSTALLED = False

TH_DEFAULT_EXCLUDE_FIELDS = getattr(settings, 'TH_DEFAULT_EXCLUDE_FIELDS', ())
