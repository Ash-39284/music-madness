from django.urls import path
from . import views

urlpatterns = [
    path('albums/<int:pk>/react/<str:reaction_type>/', views.react_to_album, name='react_to_album'),
    path('albums/<int:pk>/comment/', views.post_comment, name='post_comment'),
]