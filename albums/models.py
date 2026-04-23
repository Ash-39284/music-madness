from django.db import models

# Create your models here.
class Genre(models.Model):
    name =models.CharField(max_length=100)
    description =models.TextField(blank=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    cover_image_url = models.URLField(blank=True)
    external_id = models.CharField(max_length=255, blank=True)
    external_url = models.URLField(blank=True)
    source = models.CharField(max_length=100, blank=True) 
    is_imported = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return f"{self.artist} - {self.title}"
    
class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    external_id = models.CharField(max_length=255, blank=True)
    track_number = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    duration_seconds = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.album.title} - {self.track_number}. {self.title}"