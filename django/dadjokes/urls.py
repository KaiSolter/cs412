# File: dadjokes/urls.py
# Author: Kai Solter (ksolter@bu.edu), 4/2/2026 
# Description: URL patterns for Dad Jokes app
from django.urls import path
from dadjokes import views

# url patterns for the dadjokes app
urlpatterns = [
    path(r'', views.RandomJokeView.as_view(), name='joke'),
    path(r'random/', views.RandomJokeView.as_view(), name='random_joke'),
    path(r'jokes/', views.JokeListView.as_view(), name='all_jokes'),
    path(r'joke/<int:pk>/', views.JokeDetailView.as_view(), name='joke_detail'),
    path(r'pictures/', views.PictureListView.as_view(), name='all_pictures'),
    path(r'picture/<int:pk>/', views.PictureDetailView.as_view(), name='picture_detail'),
]