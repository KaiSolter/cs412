# File: project/urls.py
# Author: Kai Solter (ksolter@bu.edu), 4/30/2026
# Description: urls for final project app

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ArticleLandingListView.as_view(), name='landing' ),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization' ),
    path('organization/<int:pk>/follow/', FollowOrganizationView.as_view(), name='follow_organization' ),
    path('organization/<int:pk>/unfollow/', UnfollowOrganizationView.as_view(), name='unfollow_organization' ),
    path('organizations/', OrganizationListView.as_view(), name='organizations' ),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic' ),
    path('topic/<int:pk>/follow/', FollowTopicView.as_view(), name='follow_topic' ),
    path('topic/<int:pk>/unfollow/', UnfollowTopicView.as_view(), name='unfollow_topic' ),
    path('topics/', TopicListView.as_view(), name='topics' ),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article' ),
    path('article/<int:pk>/save/', SaveArticleView.as_view(), name='save_article' ),
    path('article/<int:pk>/unsave/', UnsaveArticleView.as_view(), name='unsave_article' ),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'), 
    path('profile/', ProfileSelfDetailView.as_view(), name='profile_self' ),
    path('feed/', ArticleFeedListView.as_view(), name='feed' ),
    path('followed_organizations/', FollowedOrganizationListView.as_view(), name='followed_organizations' ),
    path('followed_topics/', FollowedTopicListView.as_view(), name='followed_topics' ),
    path('saved_articles/', SavedArticlesListView.as_view(), name='saved_articles' ),
]