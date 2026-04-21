# File: project/views.py
# Author: Kai Solter (ksolter@bu.edu), 4/19/2026 
# Description: views for final project app 

from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .models import *
# Create your views here.

class OrganizationListView(ListView):
    model = Organization
    template_name = 'project/organization_list.html'
    context_object_name = 'organizations'
    
class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'project/organization_detail.html'
    context_object_name = 'organization'
    
class TopicListView(ListView):
    model = Topic
    template_name = 'project/topic_list.html'
    context_object_name = 'topics'
    
class TopicDetailView(DetailView):
    model = Topic
    template_name = 'project/topic_detail.html'
    context_object_name = 'topic'
    
class SavedArticlesListView(ListView):
    model = Article
    template_name = 'project/saved_articles.html'
    context_object_name = 'articles'
    
class ArticleFeedListView(ListView):
    model = Article
    template_name = 'project/article_feed.html'
    context_object_name = 'articles'
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'project/article_detail.html'
    context_object_name = 'article'
    
class FollowedOrganizationListView(ListView):
    model = FollowOrganization
    template_name = 'project/followed_organizations.html'
    context_object_name = 'followed_organizations'
 
class SavedArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'project/saved_articles.html'
    context_object_name = 'articles'
    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        return my_profile.saved_articles.all()
    
class ArticleFeedListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'project/article_feed.html'
    context_object_name = 'articles'
    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        followed_orgs = my_profile.get_followed_organizations()
        followed_topics = my_profile.get_followed_topics()
        return Article.objects.filter(models.Q(organization__in=followed_orgs) | models.Q(topic__in=followed_topics)).distinct()

class ProfileSelfDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

#  class FollowView(LoginRequiredMixin, View):
#     '''Create a follow relationship from the logged-in user to the target profile.'''

#     def post(self, request, *args, **kwargs):
#         target_profile = Profile.objects.get(pk=self.kwargs['pk'])
#         my_profile = Profile.objects.get(user=request.user)

#         if target_profile == my_profile:
#             return redirect('profile', pk=target_profile.pk)

#         existing = Follow.objects.filter(
#             follower_profile=my_profile,
#             profile=target_profile,
#         )

#         if not existing.exists():
#             Follow.objects.create(
#                 follower_profile=my_profile,
#                 profile=target_profile,
#             )

#         return redirect('profile', pk=target_profile.pk)