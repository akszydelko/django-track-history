from __future__ import unicode_literals
from django.conf import settings

try:
    from safedelete.signals import pre_softdelete
    DJANGO_SAFEDELETE_INSTALLED = True
except ImportError:
    # safedelete is not installed, we don't check for its signals
    DJANGO_SAFEDELETE_INSTALLED = False
    pre_softdelete = None

TH_DEFAULT_EXCLUDE_FIELDS = getattr(settings, 'TH_DEFAULT_EXCLUDE_FIELDS', ())
