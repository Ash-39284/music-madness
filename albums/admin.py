from django.contrib import admin
from .models import Genre, Album, Track

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genre', 'release_year', 'source', 'is_imported')
    list_filter = ('genre', 'source', 'is_imported')
    search_fields = ('title', 'artist')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'track_number', 'duration_seconds')
    search_fields = ('title', 'album__title')





