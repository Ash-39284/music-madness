from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from albums.models import Genre, Album
from interactions.models import Reaction, Comment



# Models tests


class ReactionModelTest(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_reaction_str(self):
        reaction = Reaction.objects.create(
            user=self.user, album=self.album, reaction_type='like'
        )
        self.assertEqual(str(reaction), 'testuser liked Black Sabbath - Paranoid')

    def test_one_reaction_per_user_per_album(self):
        Reaction.objects.create(
            user=self.user, album=self.album, reaction_type='like'
        )
        with self.assertRaises(Exception):
            Reaction.objects.create(
                user=self.user, album=self.album, reaction_type='dislike'
            )

    def test_reaction_type_like(self):
        reaction = Reaction.objects.create(
            user=self.user, album=self.album, reaction_type='like'
        )
        self.assertEqual(reaction.reaction_type, 'like')

    def test_reaction_type_dislike(self):
        reaction = Reaction.objects.create(
            user=self.user, album=self.album, reaction_type='dislike'
        )
        self.assertEqual(reaction.reaction_type, 'dislike')


class CommentModelTest(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_comment_str(self):
        comment = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Great album!'
        )
        self.assertEqual(str(comment), 'testuser on Paranoid')

    def test_top_level_comment_has_no_parent(self):
        comment = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Top level'
        )
        self.assertIsNone(comment.parent_comment)

    def test_reply_has_parent(self):
        parent = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Parent'
        )
        reply = Comment.objects.create(
            user=self.user, album=self.album,
            parent_comment=parent, comment_text='Reply'
        )
        self.assertEqual(reply.parent_comment, parent)

    def test_deleting_parent_deletes_replies(self):
        parent = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Parent'
        )
        Comment.objects.create(
            user=self.user, album=self.album,
            parent_comment=parent, comment_text='Reply'
        )
        parent.delete()
        self.assertEqual(Comment.objects.count(), 0)



# Views tests


class ReactToAlbumViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_like_creates_reaction(self):
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'like']))
        self.assertEqual(Reaction.objects.filter(
            user=self.user, album=self.album, reaction_type='like'
        ).count(), 1)

    def test_dislike_creates_reaction(self):
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'dislike']))
        self.assertEqual(Reaction.objects.filter(
            user=self.user, album=self.album, reaction_type='dislike'
        ).count(), 1)

    def test_same_reaction_twice_removes_it(self):
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'like']))
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'like']))
        self.assertEqual(Reaction.objects.filter(
            user=self.user, album=self.album
        ).count(), 0)

    def test_switching_reaction_updates_type(self):
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'like']))
        self.client.get(reverse('react_to_album', args=[self.album.pk, 'dislike']))
        reaction = Reaction.objects.get(user=self.user, album=self.album)
        self.assertEqual(reaction.reaction_type, 'dislike')

    def test_invalid_reaction_type_redirects(self):
        response = self.client.get(
            reverse('react_to_album', args=[self.album.pk, 'invalid'])
        )
        self.assertRedirects(response, reverse('album_detail', args=[self.album.pk]))

    def test_logged_out_user_redirected(self):
        self.client.logout()
        response = self.client.get(
            reverse('react_to_album', args=[self.album.pk, 'like'])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('accounts/login', response.url)

    def test_reaction_redirects_to_album_detail(self):
        response = self.client.get(
            reverse('react_to_album', args=[self.album.pk, 'like'])
        )
        self.assertRedirects(response, reverse('album_detail', args=[self.album.pk]))


class PostCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_post_comment_creates_comment(self):
        self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': 'Great album!'}
        )
        self.assertEqual(Comment.objects.filter(album=self.album).count(), 1)

    def test_post_comment_content_saved_correctly(self):
        self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': 'Great album!'}
        )
        comment = Comment.objects.get(album=self.album)
        self.assertEqual(comment.comment_text, 'Great album!')

    def test_post_empty_comment_not_saved(self):
        self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': '   '}
        )
        self.assertEqual(Comment.objects.filter(album=self.album).count(), 0)

    def test_post_reply_sets_parent(self):
        parent = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Parent comment'
        )
        self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': 'A reply', 'parent_comment_id': parent.pk}
        )
        reply = Comment.objects.get(comment_text='A reply')
        self.assertEqual(reply.parent_comment, parent)

    def test_post_comment_redirects_to_album_detail(self):
        response = self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': 'Great album!'}
        )
        self.assertRedirects(response, reverse('album_detail', args=[self.album.pk]))

    def test_logged_out_user_cannot_post_comment(self):
        self.client.logout()
        response = self.client.post(
            reverse('post_comment', args=[self.album.pk]),
            {'comment_text': 'Should not post'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.filter(album=self.album).count(), 0)


class EditCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='otheruser', password='pass')
        self.comment = Comment.objects.create(
            user=self.user, album=self.album, comment_text='Original text'
        )
        self.client.login(username='testuser', password='pass')

    def test_edit_comment_updates_text(self):
        self.client.post(
            reverse('edit_comment', args=[self.comment.pk]),
            {'comment_text': 'Updated text'}
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, 'Updated text')

    def test_edit_comment_empty_text_not_saved(self):
        self.client.post(
            reverse('edit_comment', args=[self.comment.pk]),
            {'comment_text': '   '}
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, 'Original text')

    def test_other_user_cannot_edit_comment(self):
        self.client.logout()
        self.client.login(username='otheruser', password='pass')
        response = self.client.post(
            reverse('edit_comment', args=[self.comment.pk]),
            {'comment_text': 'Hacked text'}
        )
        self.assertEqual(response.status_code, 403)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, 'Original text')

    def test_edit_comment_redirects_to_album_detail(self):
        response = self.client.post(
            reverse('edit_comment', args=[self.comment.pk]),
            {'comment_text': 'Updated text'}
        )
        self.assertRedirects(
            response, reverse('album_detail', args=[self.album.pk])
        )

    def test_logged_out_user_cannot_edit(self):
        self.client.logout()
        response = self.client.post(
            reverse('edit_comment', args=[self.comment.pk]),
            {'comment_text': 'Should not save'}
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment_text, 'Original text')


class DeleteCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Heavy Metal')
        self.album = Album.objects.create(
            title='Paranoid', artist='Black Sabbath', genre=self.genre
        )
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='otheruser', password='pass')
        self.comment = Comment.objects.create(
            user=self.user, album=self.album, comment_text='To be deleted'
        )
        self.client.login(username='testuser', password='pass')

    def test_delete_comment_removes_it(self):
        self.client.post(reverse('delete_comment', args=[self.comment.pk]))
        self.assertEqual(Comment.objects.filter(pk=self.comment.pk).count(), 0)

    def test_other_user_cannot_delete_comment(self):
        self.client.logout()
        self.client.login(username='otheruser', password='pass')
        response = self.client.post(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.filter(pk=self.comment.pk).count(), 1)

    def test_delete_comment_redirects_to_album_detail(self):
        response = self.client.post(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertRedirects(
            response, reverse('album_detail', args=[self.album.pk])
        )

    def test_logged_out_user_cannot_delete(self):
        self.client.logout()
        response = self.client.post(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.filter(pk=self.comment.pk).count(), 1)

    def test_delete_nonexistent_comment_returns_404(self):
        response = self.client.post(reverse('delete_comment', args=[99999]))
        self.assertEqual(response.status_code, 404)