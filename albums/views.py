from django.shortcuts import render, get_object_or_404
from albums.models import Album, Genre
from interactions.models import Reaction, Comment


def home_view(request):
    albums = Album.objects.filter(featured=True).exclude(cover_image_url='')[:3]
    return render(request, 'albums/home.html', {'albums': albums})


def about_view(request):
    return render(request, 'albums/about.html')

def explore_view(request):
    album_count = Album.objects.exclude(cover_image_url='').count()
    discussion_count = Comment.objects.filter(parent_comment=None).count()
    trending_albums = Album.objects.filter(featured=True).exclude(cover_image_url='')[:3]
    most_discussed = Album.objects.filter(featured=True).exclude(cover_image_url='').first()

    return render(request, 'albums/explore.html', {
        'album_count': album_count,
        'discussion_count': discussion_count,
        'trending_albums': trending_albums,
        'most_discussed': most_discussed,
    })

def genre_detail_view(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    search_query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'artist')

    albums = Album.objects.filter(genre=genre).exclude(cover_image_url='')

    if search_query:
        albums = albums.filter(title__icontains=search_query) | \
                 Album.objects.filter(genre=genre).exclude(cover_image_url='').filter(artist__icontains=search_query)

    if sort == 'title':
        albums = albums.order_by('title')
    else:
        albums = albums.order_by('artist')

    album_count = Album.objects.filter(genre=genre).exclude(cover_image_url='').count()

    return render(request, 'albums/genre_detail.html', {
        'genre': genre,
        'albums': albums,
        'album_count': album_count,
        'search_query': search_query,
        'sort': sort,
    })

def album_detail_view(request, pk):
    album = get_object_or_404(Album, pk=pk)
    tracks = album.tracks.all().order_by('track_number')
    """
    Related albums from the same genre, excluding this one.
    """
    related_albums = Album.objects.filter(
        genre=album.genre
    ).exclude(pk=album.pk).exclude(cover_image_url='')[:3]
    
    
    like_count = Reaction.objects.filter(album=album, reaction_type='like').count()
    dislike_count = Reaction.objects.filter(album=album, reaction_type='dislike').count()
    total = like_count + dislike_count
    like_percentage = round((like_count / total) * 100) if total > 0 else 0
    """
    Check current user's reaction
    """
    user_reaction = None
    if request.user.is_authenticated:
        existing = Reaction.objects.filter(user=request.user, album=album).first()
        if existing:
            user_reaction = existing.reaction_type

    comments = Comment.objects.filter(
        album=album,
        parent_comment=None
    ).order_by('-created_at')

    return render(request, 'albums/album_detail.html', {
        'album': album,
        'tracks': tracks,
        'related_albums': related_albums,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'like_percentage': like_percentage,
        'user_reaction': user_reaction,
        'comments': comments,
    })

