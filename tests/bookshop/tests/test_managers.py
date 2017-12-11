from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.test import TestCase, Client
from django.utils import timezone
from track_history.models import TrackHistoryRecord, TrackHistoryFullSnapshot

from ..models import Author

User = get_user_model()


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
        cls.before_date = timezone.now()
        cls.author_one = Author.objects.create(name='Brown')
        cls.between_date = timezone.now()
        cls.author_two = Author.objects.create(name='Anderson')
        cls.after_date = timezone.now()

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


class TrackHistoryManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_one = User.objects.create(username='John', password='JohnSecret')
        cls.user_two = User.objects.create(username='Jack', password='JackSecret')

    def test_field_history(self):
        author = Author.objects.create(name='Specter', genre=Author.GENRE_CHOICES.comedy)

        author.genre = Author.GENRE_CHOICES.fantasy
        author.save()

        author.name = 'Mark Specter'
        author.save()

        self.assertEqual(author.history.count(), 3)

        name_history = author.history.get_field_history('name')
        genre_history = author.history.get_field_history('genre')

        self.assertEqual(name_history.count(), 2)
        self.assertEqual(genre_history.count(), 2)

        self.assertDictEqual(
            name_history.last().changes,
            {
                'name': ['Specter', 'Mark Specter']
            }
        )
        self.assertDictEqual(
            genre_history.last().changes,
            {
                'genre': [Author.GENRE_CHOICES.comedy, Author.GENRE_CHOICES.fantasy]
            }
        )

    def test_creator(self):
        c_once = Client()
        c_once.force_login(self.user_one)

        response = c_once.post('/authors/', data={'name': 'Ross', 'genre': Author.GENRE_CHOICES.comedy})
        self.assertEqual(response.status_code, 201)

        author = response.json()['object']
        author = Author.objects.get(pk=author.get('id'))

        c_two = Client()
        c_two.force_login(self.user_two)
        response = c_two.post('/authors/{}/update/'.format(author.id), data={'genre': Author.GENRE_CHOICES.fantasy})
        self.assertEqual(response.status_code, 200)

        creator = author.history.get_creator()
        self.assertEqual(getattr(creator, 'id', None), self.user_one.id)

        editors = author.history.get_editors()
        self.assertEqual(len(editors), 2)
        self.assertListEqual(editors, [self.user_one, self.user_two])

