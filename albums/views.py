from django.shortcuts import render, get_object_or_404
from albums.models import Album, Genre


def home_view(request):
    albums = Album.objects.filter(featured=True).exclude(cover_image_url='')[:3]
    return render(request, 'albums/home.html', {'albums': albums})


def about_view(request):
    return render(request, 'albums/about.html')


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