from django.contrib import admin

from track_history.models import TrackHistoryFullSnapshot, TrackHistoryRecord

from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(TrackHistoryFullSnapshot)
class TrackHistoryFullSnapshotAdmin(admin.ModelAdmin):
    pass


@admin.register(TrackHistoryRecord)
class TrackHistoryRecordAdmin(admin.ModelAdmin):
    pass
