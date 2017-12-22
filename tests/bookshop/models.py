from django.db import models

from model_utils.choices import Choices
from track_history.decorators import track_changes


@track_changes
class Author(models.Model):
    GENRE_CHOICES = Choices(
        (1, 'drama', 'Drama'),
        (2, 'comedy', 'Comedy'),
        (3, 'fantasy', 'Fantasy'),
    )

    name = models.CharField(max_length=255)
    genre = models.PositiveSmallIntegerField(choices=GENRE_CHOICES, default=GENRE_CHOICES.comedy)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


@track_changes
class Book(models.Model):
    name = models.CharField(max_length=255)
    isbn_number = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
