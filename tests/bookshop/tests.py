from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from track_history.models import TrackHistoryRecord

from .models import Author


class BasicOperationsTestCase(TestCase):
    def test_object_creation(self):
        christie = Author.objects.create(name="Christie", genre=Author.GENRE_CHOICES.drama)
        christie_history = christie.history.last()

        self.assertEqual(christie.history.count(), 1)
        self.assertEqual(christie, christie_history.current_instance)
        self.assertEqual(christie_history.record_type, TrackHistoryRecord.RECORD_TYPES.created)
        self.assertDictEqual(
            christie_history.changes,
            {
                'id': [None, christie.id],
                'name': [None, 'Christie'],
                'genre': [None, Author.GENRE_CHOICES.drama]
            }
        )
        self.assertDictEqual(
            christie_history.full_snapshot.history_data,
            {
                'id': christie.id,
                'name': 'Christie',
                'genre': Author.GENRE_CHOICES.drama
            }
        )

    def test_object_modifications(self):
        king = Author.objects.create(name="King", genre=Author.GENRE_CHOICES.drama)
        king.genre = Author.GENRE_CHOICES.comedy
        king.save()

        king_history = king.history.last()

        self.assertEqual(king.history.count(), 2)
        self.assertEqual(king_history.record_type, TrackHistoryRecord.RECORD_TYPES.modified)
        self.assertDictEqual(
            king_history.changes,
            {
                'genre': [Author.GENRE_CHOICES.drama, Author.GENRE_CHOICES.comedy]
            }
        )

        self.assertDictEqual(
            king_history.full_snapshot.history_data,
            {
                'id': king.id,
                'name': 'King',
                'genre': Author.GENRE_CHOICES.comedy
            }
        )

        king.name = 'Stephen King'
        king.save()

        king_history = king.history.last()

        self.assertEqual(king.history.count(), 3)
        self.assertEqual(king_history.record_type, TrackHistoryRecord.RECORD_TYPES.modified)
        self.assertDictEqual(
            king_history.changes,
            {
                'name': ['King', 'Stephen King']
            }
        )

        self.assertDictEqual(
            king_history.full_snapshot.history_data,
            {
                'id': king.id,
                'name': 'Stephen King',
                'genre': Author.GENRE_CHOICES.comedy
            }
        )

        king.name = 'King'
        king.save()

        king_history = king.history.last()

        self.assertEqual(king.history.count(), 4)
        self.assertEqual(king_history.record_type, TrackHistoryRecord.RECORD_TYPES.modified)
        self.assertDictEqual(
            king_history.changes,
            {
                'name': ['Stephen King', 'King']
            }
        )

        self.assertDictEqual(
            king_history.full_snapshot.history_data,
            {
                'id': king.id,
                'name': 'King',
                'genre': Author.GENRE_CHOICES.comedy
            }
        )

    def test_object_deletion(self):
        gordon = Author.objects.create(name="Gordon")
        object_id = gordon.id
        history_qs = TrackHistoryRecord.objects.filter(content_type=ContentType.objects.get_for_model(gordon), object_id_int=object_id)
        gordon.delete()

        gordon_history = history_qs.last()

        self.assertEqual(history_qs.count(), 2)
        self.assertEqual(gordon_history.record_type, TrackHistoryRecord.RECORD_TYPES.deleted)
        self.assertDictEqual(
            gordon_history.changes,
            {
                'id': [object_id, None],
                'name': ['Gordon', None],
                'genre': [Author.GENRE_CHOICES.comedy, None]
            }
        )

        self.assertDictEqual(
            gordon_history.full_snapshot.history_data,
            {
                'id': object_id,
                'name': 'Gordon',
                'genre': Author.GENRE_CHOICES.comedy
            }
        )


class BasicOperationsOnDeferredModelTestCase(TestCase):
    def test_deferred_object_modifications(self):
        king = Author.objects.create(name="King", genre=Author.GENRE_CHOICES.drama)
        king = Author.objects.only('genre').get(pk=king.pk)
        king.genre = Author.GENRE_CHOICES.comedy
        king.save()

        king_history = king.history.last()

        self.assertEqual(king.history.count(), 2)
        self.assertEqual(king_history.record_type, TrackHistoryRecord.RECORD_TYPES.modified)
        self.assertDictEqual(
            king_history.changes,
            {
                'genre': [Author.GENRE_CHOICES.drama, Author.GENRE_CHOICES.comedy]
            }
        )

        self.assertDictEqual(
            king_history.full_snapshot.history_data,
            {
                'id': king.id,
                'name': 'King',
                'genre': Author.GENRE_CHOICES.comedy
            }
        )


class FailingOperationsTestCase(TestCase):
    def test_failed_object_creation(self):
        with self.settings(TH_RECORD_MODEL='bookshop.utils.CreationFailTestingTrackHistoryRecord'):
            try:
                Author.objects.create(name="Smith")
                self.fail('Expected Exception did not occurred.')
            except RuntimeError:
                pass

        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(name="Smith")

    def test_failed_object_modifications(self):
        with self.settings(TH_RECORD_MODEL='bookshop.utils.ModificationFailTestingTrackHistoryRecord'):
            author = Author.objects.create(name="Joe")
            try:
                author.genre = Author.GENRE_CHOICES.drama
                author.save()
                self.fail('Expected Exception did not occurred.')
            except RuntimeError:
                pass

        self.assertEqual(author.genre, Author.GENRE_CHOICES.drama)

        true_author = Author.objects.get(name="Joe")
        self.assertEqual(true_author.genre, Author.GENRE_CHOICES.comedy)

    # TODO: Implement failed object deletion tests
    # As Track History uses pre_delete signal,
    # the history record is created before real object change is handled in database
    # (as opposite to creation and modification options)
    # Therefore it's hard to raise an error during model deletion
    # (after pre_delete signal is fired and the model is being actually deleted).
    # But django is doing a great job wrapping signals execution and object deletion
    # into an atomic block, so technically the data should be consistent
    # if an error during deletion will occur.
    # See: django.db.models.deletion.Collector#delete function
