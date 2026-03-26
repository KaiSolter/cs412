# File: mini_insta/forms.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: Forms for mini_insta app 

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''
    Form for creating a new article.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']

class UpdateArticleForm(forms.ModelForm):
    '''
    Form for updating an existing article.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Article
        fields = ['title', 'text']

class CreateCommentForm(forms.ModelForm):
    '''
    Form for creating a new comment.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Comment
        fields = ['author', 'text']