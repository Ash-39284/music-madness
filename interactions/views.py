from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
            # Same reaction — remove it (toggle off)
            existing.delete()
        else:
            # Different reaction — update it
            existing.reaction_type = reaction_type
            existing.save()
    else:
        # No existing reaction — create new
        Reaction.objects.create(
            user=request.user,
            album=album,
            reaction_type=reaction_type
        )
    
    return redirect('album_detail', pk=pk)


@login_required
def PostComment(request, pk):
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