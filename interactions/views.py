from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from albums.models import Album
from .models import Reaction, Comment


@login_required
def react_to_album(request, pk, reaction_type):
    album = get_object_or_404(Album, pk=pk)

    if reaction_type not in ['like', 'dislike']:
        return redirect('album_detail', pk=pk)

    existing = Reaction.objects.filter(user=request.user, album=album).first()

    if existing:
        if existing.reaction_type == reaction_type:
            existing.delete()
        else:
            existing.reaction_type = reaction_type
            existing.save()
    else:
        Reaction.objects.create(
            user=request.user,
            album=album,
            reaction_type=reaction_type
        )

    return redirect('album_detail', pk=pk)


@login_required
def post_comment(request, pk):
    album = get_object_or_404(Album, pk=pk)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        parent_id = request.POST.get('parent_comment_id')

        if comment_text:
            parent = None
            if parent_id:
                parent = Comment.objects.filter(pk=parent_id).first()

            Comment.objects.create(
                user=request.user,
                album=album,
                parent_comment=parent,
                comment_text=comment_text,
            )

    return redirect('album_detail', pk=pk)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Only the comment owner can edit
    if comment.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        if comment_text:
            comment.comment_text = comment_text
            comment.save()

    return redirect('album_detail', pk=comment.album.pk)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Only the comment owner can delete
    if comment.user != request.user:
        return HttpResponseForbidden()

    album_pk = comment.album.pk
    comment.delete()
    return redirect('album_detail', pk=album_pk)