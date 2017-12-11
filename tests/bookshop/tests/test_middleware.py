from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Author

User = get_user_model()


class TrackHistoryManagerTestCase(TestCase):
    def test_storing_user_in_thread_local_middleware(self):
        user = User.objects.create(username='Mark', password='MarkSecret')
        c = Client()
        c.force_login(user)

        response = c.post('/authors/', data={'name': 'Kate', 'genre': Author.GENRE_CHOICES.comedy})
        self.assertEqual(response.status_code, 201)

        author = response.json()['object']
        author = Author.objects.get(pk=author.get('id'))
        author_history = author.history.last()

        self.assertEqual(getattr(author_history.user, 'id', None), user.id)
