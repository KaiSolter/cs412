from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''
    Form for creating a new article.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']
        
class CreateCommentForm(forms.ModelForm):
    '''
    Form for creating a new comment.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Comment
        fields = ['author', 'text']