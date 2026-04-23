from django.shortcuts import render
from albums.models import Album

# Create your views here.
def home_view(request):
    albums = Album.objects.filter(featured=True, ).exclude(cover_image_url='')[:3]
    return render(request, 'albums/home.html', {'albums': albums})

def about_view(request):
    return render(request, 'albums/about.html')


