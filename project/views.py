# File: project/views.py
# Author: Kai Solter (ksolter@bu.edu), 4/19/2026 
# Description: views for final project app 

from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
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
    

