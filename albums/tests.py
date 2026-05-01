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

class TrackModelTest(TestCase):
 
    def setUp(self):
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid',
            artist='Black Sabbath',
            genre=self.genre,
        )
        self.track = Track.objects.create(
            album=self.album,
            title='War Pigs',
            track_number=1,
            duration_seconds=478,
        )
 
    def test_track_str(self):
        self.assertEqual(str(self.track), 'Paranoid - 1. War Pigs')
 
    def test_track_belongs_to_album(self):
        self.assertEqual(self.track.album, self.album)

# View tests

class HomeViewTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
 
    def test_home_view_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
 
    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'albums/home.html')
 
    def test_home_view_shows_featured_albums_only(self):
        Album.objects.create(
            title='Featured Album', artist='Artist A',
            genre=self.genre, featured=True,
            cover_image_url='http://example.com/cover.jpg'
        )
        Album.objects.create(
            title='Unfeatured Album', artist='Artist B',
            genre=self.genre, featured=False,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(reverse('home'))
        albums = response.context['albums']
        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0].title, 'Featured Album')
 
    def test_home_view_excludes_albums_without_cover(self):
        Album.objects.create(
            title='No Cover', artist='Artist A',
            genre=self.genre, featured=True, cover_image_url=''
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['albums']), 0)
 
    def test_home_view_max_three_albums(self):
        for i in range(5):
            Album.objects.create(
                title=f'Album {i}', artist='Artist',
                genre=self.genre, featured=True,
                cover_image_url='http://example.com/cover.jpg'
            )
        response = self.client.get(reverse('home'))
        self.assertLessEqual(len(response.context['albums']), 3)
 
 
class AboutViewTest(TestCase):
 
    def test_about_view_status_200(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
 
    def test_about_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'albums/about.html')
 
 
class ExploreViewTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
 
    def test_explore_view_status_200(self):
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.status_code, 200)
 
    def test_explore_view_uses_correct_template(self):
        response = self.client.get(reverse('explore'))
        self.assertTemplateUsed(response, 'albums/explore.html')
 
    def test_explore_view_album_count_excludes_no_cover(self):
        Album.objects.create(
            title='With Cover', artist='Artist A',
            genre=self.genre, cover_image_url='http://example.com/cover.jpg'
        )
        Album.objects.create(
            title='No Cover', artist='Artist B',
            genre=self.genre, cover_image_url=''
        )
        response = self.client.get(reverse('explore'))
        self.assertEqual(response.context['album_count'], 1)
 
    def test_explore_view_discussion_count(self):
        user = User.objects.create_user(username='testuser', password='pass')
        album = Album.objects.create(
            title='Test Album', artist='Artist',
            genre=self.genre, cover_image_url='http://example.com/cover.jpg'
        )
        Comment.objects.create(user=user, album=album, comment_text='Top level')
        parent = Comment.objects.filter(album=album).first()
        Comment.objects.create(
            user=user, album=album,
            parent_comment=parent, comment_text='Reply'
        )
        response = self.client.get(reverse('explore'))
        # Only top-level comments counted
        self.assertEqual(response.context['discussion_count'], 1)
 
    def test_explore_view_context_keys(self):
        response = self.client.get(reverse('explore'))
        self.assertIn('album_count', response.context)
        self.assertIn('discussion_count', response.context)
        self.assertIn('trending_albums', response.context)
        self.assertIn('most_discussed', response.context)
 
 
class GenreDetailViewTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath',
            genre=self.genre,
            cover_image_url='http://example.com/cover.jpg'
        )
 
    def test_genre_detail_status_200(self):
        response = self.client.get(reverse('genre_detail', args=['heavy-metal']))
        self.assertEqual(response.status_code, 200)
 
    def test_genre_detail_404_for_invalid_slug(self):
        response = self.client.get(reverse('genre_detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)
 
    def test_genre_detail_uses_correct_template(self):
        response = self.client.get(reverse('genre_detail', args=['heavy-metal']))
        self.assertTemplateUsed(response, 'albums/genre_detail.html')
 
    def test_genre_detail_shows_correct_albums(self):
        other_genre = Genre.objects.create(name='Thrash')
        Album.objects.create(
            title='Other Album', artist='Other Artist',
            genre=other_genre,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(reverse('genre_detail', args=['heavy-metal']))
        albums = response.context['albums']
        self.assertEqual(albums.count(), 1)
        self.assertEqual(albums[0].title, 'Paranoid')
 
    def test_genre_detail_search_by_title(self):
        Album.objects.create(
            title='Master of Puppets', artist='Metallica',
            genre=self.genre,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(
            reverse('genre_detail', args=['heavy-metal']), {'q': 'paranoid'}
        )
        albums = response.context['albums']
        self.assertTrue(any(a.title == 'Paranoid' for a in albums))
 
    def test_genre_detail_search_by_artist(self):
        response = self.client.get(
            reverse('genre_detail', args=['heavy-metal']), {'q': 'Black Sabbath'}
        )
        albums = response.context['albums']
        self.assertTrue(any(a.artist == 'Black Sabbath' for a in albums))
 
    def test_genre_detail_sort_by_title(self):
        Album.objects.create(
            title='Alchemy', artist='Zebra',
            genre=self.genre,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(
            reverse('genre_detail', args=['heavy-metal']), {'sort': 'title'}
        )
        albums = list(response.context['albums'])
        self.assertEqual(albums[0].title, 'Alchemy')
 
    def test_genre_detail_sort_by_artist_default(self):
        Album.objects.create(
            title='Back in Black', artist='AC/DC',
            genre=self.genre,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(reverse('genre_detail', args=['heavy-metal']))
        albums = list(response.context['albums'])
        self.assertEqual(albums[0].artist, 'AC/DC')
 
    def test_genre_detail_excludes_albums_without_cover(self):
        Album.objects.create(
            title='No Cover Album', artist='No Cover Artist',
            genre=self.genre, cover_image_url=''
        )
        response = self.client.get(reverse('genre_detail', args=['heavy-metal']))
        for album in response.context['albums']:
            self.assertNotEqual(album.cover_image_url, '')
 
 
class AlbumDetailViewTest(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath',
            genre=self.genre,
            cover_image_url='http://example.com/cover.jpg'
        )
        self.user = User.objects.create_user(username='testuser', password='pass')
 
    def test_album_detail_status_200(self):
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertEqual(response.status_code, 200)
 
    def test_album_detail_404_for_invalid_pk(self):
        response = self.client.get(reverse('album_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
 
    def test_album_detail_uses_correct_template(self):
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertTemplateUsed(response, 'albums/album_detail.html')
 
    def test_album_detail_context_keys(self):
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        for key in ['album', 'tracks', 'related_albums', 'like_count',
                    'dislike_count', 'like_percentage', 'user_reaction', 'comments']:
            self.assertIn(key, response.context)
 
    def test_album_detail_like_percentage_zero_with_no_reactions(self):
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertEqual(response.context['like_percentage'], 0)
 
    def test_album_detail_like_percentage_with_reactions(self):
        Reaction.objects.create(user=self.user, album=self.album, reaction_type='like')
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertEqual(response.context['like_percentage'], 100)
 
    def test_album_detail_user_reaction_none_when_logged_out(self):
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertIsNone(response.context['user_reaction'])
 
    def test_album_detail_user_reaction_shown_when_logged_in(self):
        Reaction.objects.create(user=self.user, album=self.album, reaction_type='like')
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        self.assertEqual(response.context['user_reaction'], 'like')
 
    def test_album_detail_related_albums_from_same_genre(self):
        other = Album.objects.create(
            title='Master of Puppets', artist='Metallica',
            genre=self.genre,
            cover_image_url='http://example.com/cover2.jpg'
        )
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        related = list(response.context['related_albums'])
        self.assertIn(other, related)
        self.assertNotIn(self.album, related)
 
    def test_album_detail_comments_top_level_only(self):
        parent = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Top level'
        )
        Comment.objects.create(
            user=self.user, album=self.album,
            parent_comment=parent, comment_text='Reply'
        )
        response = self.client.get(reverse('album_detail', args=[self.album.pk]))
        comments = response.context['comments']
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments[0].comment_text, 'Top level')
 