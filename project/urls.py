# File: project/urls.py
# Author: Kai Solter (ksolter@bu.edu), 4/19/2026 
# Description: urls for final project app 

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization' ),
    path('organizations/', OrganizationListView.as_view(), name='organizations' ),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic' ),
    path('topics/', TopicListView.as_view(), name='topics' ),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    #next page is organizations for now, but should be the generic landing page for the app once that is implemented
    path('logout/', auth_views.LogoutView.as_view(next_page='organizations'), name='logout'), 
    path('profile/', ProfileSelfDetailView.as_view(), name='profile_self' ),
]