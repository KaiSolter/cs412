from xml.etree.ElementTree import Comment

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from . forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

class showAll(ListView):
    '''显示所有文章'''
    model = Article
    template_name = 'blog/showAll.html'
    context_object_name = 'articles'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): {request.user} ')
        else:
            print('ShowAllView.dispatch(): Not Logged In')
        return super().dispatch(request, *args, **kwargs)
    
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
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''
    Display html form to user and process submission storing the new data object
    '''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    
    def get_login_url(self):
        return reverse('login')
    
    def form_valid(self, form):
        '''If the form is valid, save the associated model'''
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')
        
        user = self.request.user
        form.instance.user = user
        
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    '''
    Display html form to user and process submission updating the existing data object
    '''
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

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

class DeleteCommentView(DeleteView):
    '''
    Docstring for DeleteCommentView
    '''
    model = Comment 
    template_name = "blog/delete_comment_form.html"
    def get_success_url(self):
        '''After successfully deleting a comment, redirect to the article page
        '''
        # find primary key for comment
        pk = self.kwargs['pk']
        #find comment object
        comment = Comment.objects.get(pk=pk)
        #find article associated with comment
        article = comment.article
        return reverse('article', kwargs={'pk': article.pk})
    
class UserRegisterView(CreateView):
    '''
    Docstring for UserRegisterView
    '''
    form_class = UserCreationForm
    template_name = "blog/register.html"
    model = User
    
    def get_success_url(self):
        return reverse('login')