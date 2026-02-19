from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from . forms import CreateArticleForm
import random
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
    