from track_history.models import TrackHistoryRecord


class CreationFailTestingTrackHistoryRecord(TrackHistoryRecord):
    def save(self, *args, **kwargs):
        if self.record_type == self.RECORD_TYPES.created:
            raise RuntimeError
        return super(CreationFailTestingTrackHistoryRecord, self).save(*args, **kwargs)

    class Meta:
        proxy = True


class ModificationFailTestingTrackHistoryRecord(TrackHistoryRecord):
    def save(self, *args, **kwargs):
        if self.record_type == self.RECORD_TYPES.modified:
            raise RuntimeError
        return super(ModificationFailTestingTrackHistoryRecord, self).save(*args, **kwargs)

    class Meta:
        proxy = True
