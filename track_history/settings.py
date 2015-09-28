from __future__ import unicode_literals
from django.conf import settings

TH_DEFAULT_EXCLUDE_FIELDS = getattr(settings, 'TH_DEFAULT_EXCLUDE_FIELDS', ())
