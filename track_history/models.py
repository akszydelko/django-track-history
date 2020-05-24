from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models, OperationalError
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices

from .manager import TrackHistorySnapshotManager, TrackHistoryRecordManager

UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class TrackHistoryFullSnapshot(models.Model):
    history_data = JSONField()

    objects = TrackHistorySnapshotManager()

    def __str__(self):
        return 'Fill snapshot of track history record with id {}'.format(self.id)

    class Meta:
        app_label = 'track_history'


class TrackHistoryRecord(models.Model):
    RECORD_TYPES = Choices(
        (0, 'created', _('Created')),
        (1, 'modified', _('Modified')),
        (2, 'deleted', _('Deleted'))
    )

    full_snapshot = models.OneToOneField(TrackHistoryFullSnapshot, primary_key=True, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('date created'),
                                        help_text='The date and time this record was created.')
    object_id = models.TextField(db_index=True, help_text='Primary key of the model under track history control.')
    object_id_int = models.IntegerField(blank=True, null=True, db_index=True,
                                        help_text='An indexed, integer version of the stored model\'s primary key, used for faster lookups.')
    content_type = models.ForeignKey(ContentType, help_text='Content type of the model under track history control.', on_delete=models.PROTECT)
    user = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL, verbose_name=_('user'),
                             help_text='The user who created this record.', related_name='+')
    record_type = models.PositiveSmallIntegerField(choices=RECORD_TYPES)
    changes = JSONField(default=dict)

    # A link to the current instance
    current_instance = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    objects = TrackHistoryRecordManager()

    def __str__(self):
        return 'History track record of {}({})'.format(
            ContentType.objects.get_for_id(self.content_type_id).model_class().__name__, self.object_id)

    def save(self, *args, **kwargs):
        snapshot_id = TrackHistoryFullSnapshot.objects.create_snapshot_for_model(
            model=self.content_type.model_class(), raw_id=self.object_id)
        if not snapshot_id:
            raise OperationalError('Snapshot was not saved properly.')
        self.full_snapshot_id = snapshot_id
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'track_history'
