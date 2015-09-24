from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_pgjsonb import JSONField as JSONBField
from django.utils.translation import ugettext_lazy as _
from model_utils.choices import Choices

UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class TrackHistoryRecord(models.Model):
    RECORD_TYPES = Choices(
        (0, 'created', _("Created")),
        (1, 'modified', _("Modified")),
        (2, 'deleted', _("Deleted"))
    )

    date_created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("date created"),
                                        help_text="The date and time this record was created.")
    object_id = models.TextField(help_text="Primary key of the model under track history control.")
    object_id_int = models.IntegerField(blank=True, null=True, db_index=True,
                                        help_text="An indexed, integer version of the stored model's primary key, used for faster lookups.")
    content_type = models.ForeignKey(ContentType, help_text="Content type of the model under track history control.")
    user = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, verbose_name=_("user"),
                             help_text="The user who created this record.", related_name='+')
    history_data = JSONBField()
    record_type = models.PositiveSmallIntegerField(choices=RECORD_TYPES)
    changes = JSONBField(default={})

    # A link to the current instance
    current_instance = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    def __str__(self):
        return "History track record of %s(%s)" % (
            ContentType.objects.get_for_id(self.content_type_id).model_class().__name__, self.object_id)


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
