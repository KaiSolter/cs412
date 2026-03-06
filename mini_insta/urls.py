# File: mini_insta/urls.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: urls for mini_insta app 

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProfileListView.as_view() , name='profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile' ),
    path('profile', ProfileSelfDetailView.as_view(), name='profile_self' ),
    path('post/<int:pk>', PostDetailView.as_view(), name='post' ),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='profiles'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]