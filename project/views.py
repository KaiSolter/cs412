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
from django.urls import reverse_lazy

import os
import requests

from .models import *
from .forms import ArticleSearchForm, ProfileUpdateForm
from .utils import classify_topic
# Create your views here.


NEWSAPI_URL = 'https://newsapi.org/v2/everything'


def search_newsapi(query):
    """
    Search NewsAPI for articles matching query, import them all into the local DB
    (deduplicating by URL), and return status metadata plus imported Article objects.
    """
    api_key = os.environ.get('NEWSAPI_KEY', '')
    if not api_key:
        return {
            'articles': [],
            'error': 'NEWSAPI_KEY is not set on the server.',
            'fetched_count': 0,
            'imported_count': 0,
            'existing_count': 0,
        }

    try:
        response = requests.get(
            NEWSAPI_URL,
            params={'q': query, 'pageSize': 20, 'language': 'en', 'sortBy': 'publishedAt', 'apiKey': api_key},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        return {
            'articles': [],
            'error': f'NewsAPI request failed: {exc}',
            'fetched_count': 0,
            'imported_count': 0,
            'existing_count': 0,
        }

    imported = []
    imported_count = 0
    existing_count = 0
    fetched_count = len(data.get('articles', []))
    for item in data.get('articles', []):
        url = (item.get('url') or '').strip()
        title = (item.get('title') or '').strip()
        description = (item.get('description') or '').strip()
        source_name = ((item.get('source') or {}).get('name') or 'Unknown').strip()

        if not url or not title:
            continue

        # Return existing article if already in DB
        existing = Article.objects.filter(url=url).first()
        if existing:
            imported.append(existing)
            existing_count += 1
            continue

        org, _ = Organization.objects.get_or_create(
            name=source_name,
            defaults={'independent': True},
        )
        topic = classify_topic(title + ' ' + description)
        article = Article.objects.create(
            title=title,
            url=url,
            summary=description,
            full_text='',
            organization=org,
            topic=topic,
        )
        imported.append(article)
        imported_count += 1

    return {
        'articles': imported,
        'error': '',
        'fetched_count': fetched_count,
        'imported_count': imported_count,
        'existing_count': existing_count,
    }

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
        profile, _ = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={'username': self.request.user.username},
        )
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'project/profile_form.html'
    success_url = reverse_lazy('profile_self')

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(
            user=self.request.user,
            defaults={'username': self.request.user.username},
        )
        return profile


class ArticleSearchView(View):
    template_name = 'project/article_search.html'

    def get(self, request):
        form = ArticleSearchForm()
        return render(request, self.template_name, {
            'form': form,
            'results': None,
            'external_results': [],
            'external_meta': None,
        })

    def post(self, request):
        form = ArticleSearchForm(request.POST)
        results = []
        external_results = []
        external_meta = None
        if form.is_valid():
            query = form.cleaned_data['query'].strip()
            include_external = form.cleaned_data.get('include_external', False)
            if query:
                results = list(
                    Article.objects.filter(
                        models.Q(title__icontains=query)
                        | models.Q(summary__icontains=query)
                        | models.Q(full_text__icontains=query)
                    )
                    .select_related('organization', 'topic')
                    .order_by('-published_date')
                )
                if include_external:
                    local_pks = {a.pk for a in results}
                    external_payload = search_newsapi(query)
                    external_articles = external_payload['articles']
                    # Only show external articles not already in local results
                    external_results = [a for a in external_articles if a.pk not in local_pks]
                    external_meta = {
                        'error': external_payload['error'],
                        'fetched_count': external_payload['fetched_count'],
                        'imported_count': external_payload['imported_count'],
                        'existing_count': external_payload['existing_count'],
                        'shown_count': len(external_results),
                    }
        return render(request, self.template_name, {
            'form': form,
            'results': results,
            'external_results': external_results,
            'external_meta': external_meta,
        })