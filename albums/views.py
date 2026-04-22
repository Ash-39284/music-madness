from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'albums/home.html')

def about_view(request):
    return render(request, 'albums/about.html')