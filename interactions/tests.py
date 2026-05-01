from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from albums.models import Genre, Album
from interactions.models import Reaction, Comment


# Model views

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