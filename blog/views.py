from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from . forms import CreateArticleForm, CreateCommentForm
import random
from django.urls import reverse
# Create your views here.

class showAll(ListView):
    '''显示所有文章'''
    model = Article
    template_name = 'blog/showAll.html'
    context_object_name = 'articles'
    
class ArticleView(DetailView):
    '''
    Docstring for Article
    '''
    model = Article
    template_name = "blog/article.html"
    context_object_name = 'article'
    
class RandomArticleView(DetailView):
    '''
    Docstring for RandomArticleView
    '''
    model = Article
    template_name = "blog/article.html"
    context_object_name = 'article'
    def get_object(self):
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
class CreateArticleView(CreateView):
    '''
    Display html form to user and process submission storing the new data object
    '''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

class CreateCommentView(CreateView):
    '''
    Display html form to user and process submission storing the new data object
    '''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_success_url(self):
        '''After successfully creating a comment, redirect to the article page
        '''
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''Associate the comment with the correct article before saving'''
        print(form.cleaned_data)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        form.instance.article = article
        return super().form_valid(form)
    