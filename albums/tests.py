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

class AlbumModelTest(TestCase):
 
    def setUp(self):
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid',
            artist='Black Sabbath',
            genre=self.genre,
            release_year=1970,
        )
 
    def test_album_str(self):
        self.assertEqual(str(self.album), 'Black Sabbath - Paranoid')
 
    def test_like_count_no_reactions(self):
        self.assertEqual(self.album.like_count(), 0)
 
    def test_dislike_count_no_reactions(self):
        self.assertEqual(self.album.dislike_count(), 0)
 
    def test_like_count_with_reactions(self):
        user = User.objects.create_user(username='testuser', password='pass')
        Reaction.objects.create(user=user, album=self.album, reaction_type='like')
        self.assertEqual(self.album.like_count(), 1)
 
    def test_dislike_count_with_reactions(self):
        user = User.objects.create_user(username='testuser', password='pass')
        Reaction.objects.create(user=user, album=self.album, reaction_type='dislike')
        self.assertEqual(self.album.dislike_count(), 1)
 
    def test_comment_count_no_comments(self):
        self.assertEqual(self.album.comment_count(), 0)
 
    def test_comment_count_top_level_only(self):
        user = User.objects.create_user(username='testuser', password='pass')
        parent = Comment.objects.create(
            user=user, album=self.album, comment_text='Top level comment'
        )
        # Reply should not be counted
        Comment.objects.create(
            user=user, album=self.album,
            parent_comment=parent, comment_text='A reply'
        )
        self.assertEqual(self.album.comment_count(), 1)
 
    def test_album_featured_default_false(self):
        self.assertFalse(self.album.featured)
 
    def test_album_is_imported_default_false(self):
        self.assertFalse(self.album.is_imported)