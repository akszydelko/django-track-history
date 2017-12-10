from datetime import datetime

from django.forms import model_to_dict
from django.test import TestCase
from track_history.models import TrackHistoryRecord, TrackHistoryFullSnapshot

from ..models import Author


class HistorySnapshotTestCase(TestCase):
    def test_history_snapshot_creation(self):
        author = Author.objects.create(name='Bing')

        snapshot_pk = TrackHistoryFullSnapshot.objects.create_snapshot_for_model(
            model=Author, raw_id=author.id)

        self.assertDictEqual(
            TrackHistoryFullSnapshot.objects.get(pk=snapshot_pk).history_data,
            model_to_dict(author)
        )


class HistorySnapshotManagerForbiddenMethodsTestCase(TestCase):
    def test_history_snapshot_creation(self):
        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.create()

        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.bulk_create()

        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.get_or_create()

    def test_history_snapshot_modification(self):
        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.update()

        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.all().update()

    def test_history_snapshot_deletion(self):
        with self.assertRaises(AttributeError):
            TrackHistoryFullSnapshot.objects.delete()

        with self.assertRaises(NotImplementedError):
            TrackHistoryFullSnapshot.objects.all().delete()


class DateManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.before_date = datetime.now()
        cls.author_one = Author.objects.create(name='Brown')
        cls.between_date = datetime.now()
        cls.author_two = Author.objects.create(name='Anderson')
        cls.after_date = datetime.now()

    def test_in_date_method(self):
        self.assertEqual(TrackHistoryRecord.objects.in_dates(self.before_date, self.between_date).count(), 1)
        self.assertEqual(TrackHistoryRecord.objects.in_dates(self.before_date, self.after_date).count(), 2)

    def test_before_date_method(self):
        self.assertEqual(TrackHistoryRecord.objects.before_date(self.before_date).count(), 0)
        self.assertEqual(TrackHistoryRecord.objects.before_date(self.between_date).count(), 1)
        self.assertEqual(TrackHistoryRecord.objects.before_date(self.after_date).count(), 2)

    def test_after_date_method(self):
        self.assertEqual(TrackHistoryRecord.objects.after_date(self.before_date).count(), 2)
        self.assertEqual(TrackHistoryRecord.objects.after_date(self.between_date).count(), 1)
        self.assertEqual(TrackHistoryRecord.objects.after_date(self.after_date).count(), 0)
