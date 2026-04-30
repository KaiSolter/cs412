# File: project/views.py
# Author: Kai Solter (ksolter@bu.edu), 4/30/2026
# Description: views for final project app

from django.shortcuts import render, redirect, get_object_or_404
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = (
            Article.objects.filter(organization=self.object)
            .select_related('organization', 'topic')
            .order_by('-published_date')
        )
        context['is_following'] = False
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            if my_profile:
                context['is_following'] = FollowOrganization.objects.filter(
                    profile=my_profile, organization=self.object
                ).exists()
        return context


class FollowOrganizationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        my_profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'username': request.user.username}
        )
        FollowOrganization.objects.get_or_create(profile=my_profile, organization=organization)
        return redirect('organization', pk=organization.pk)


class UnfollowOrganizationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        my_profile = Profile.objects.filter(user=request.user).first()
        if my_profile:
            FollowOrganization.objects.filter(profile=my_profile, organization=organization).delete()
        return redirect('organization', pk=organization.pk)
    
class TopicListView(ListView):
    model = Topic
    template_name = 'project/topic_list.html'
    context_object_name = 'topics'
    
class TopicDetailView(DetailView):
    model = Topic
    template_name = 'project/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = (
            Article.objects.filter(topic=self.object)
            .select_related('organization', 'topic')
            .order_by('-published_date')
        )
        context['is_following'] = False
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            if my_profile:
                context['is_following'] = FollowTopic.objects.filter(
                    profile=my_profile, topic=self.object
                ).exists()
        return context


class FollowTopicView(LoginRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        my_profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'username': request.user.username}
        )
        FollowTopic.objects.get_or_create(profile=my_profile, topic=topic)
        return redirect('topic', pk=topic.pk)


class UnfollowTopicView(LoginRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        my_profile = Profile.objects.filter(user=request.user).first()
        if my_profile:
            FollowTopic.objects.filter(profile=my_profile, topic=topic).delete()
        return redirect('topic', pk=topic.pk)

class ArticleLandingListView(ListView):
    model = Article
    template_name = 'project/article_landing.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.all().order_by('-published_date')
    
class ArticleFeedListView(ListView):
    model = Article
    template_name = 'project/article_feed.html'
    context_object_name = 'articles'
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'project/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_article_saved'] = False

        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            if my_profile:
                context['is_article_saved'] = my_profile.saved_articles.filter(pk=self.object.pk).exists()

        return context


class SaveArticleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        my_profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'username': request.user.username}
        )
        my_profile.saved_articles.add(article)
        return redirect('article', pk=article.pk)


class UnsaveArticleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        my_profile = Profile.objects.filter(user=request.user).first()
        if my_profile:
            my_profile.saved_articles.remove(article)
        return redirect('article', pk=article.pk)

class FollowedOrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'project/followed_organizations.html'
    context_object_name = 'organizations'

    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        return my_profile.get_followed_organizations()


class FollowedTopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'project/followed_topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        return my_profile.get_followed_topics()
 
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