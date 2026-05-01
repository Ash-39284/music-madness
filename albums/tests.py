from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from albums.models import Genre, Album, Track
from interactions.models import Comment, Reaction

# Model Tests

class GenreModelTest(TestCase):
 
    def test_genre_str(self):
        genre = Genre.objects.create(name='Heavy Metal')
        self.assertEqual(str(genre), 'Heavy Metal')
 
    def test_genre_slug_auto_generated(self):
        genre = Genre.objects.create(name='Heavy Metal')
        self.assertEqual(genre.slug, 'heavy-metal')
 
    def test_genre_slug_not_overwritten_on_save(self):
        genre = Genre.objects.create(name='Heavy Metal')
        genre.save()
        self.assertEqual(genre.slug, 'heavy-metal')
 
    def test_genre_slug_unique(self):
        Genre.objects.create(name='Heavy Metal')
        with self.assertRaises(Exception):
            Genre.objects.create(name='Heavy Metal')