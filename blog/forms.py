from django import forms
from .models import Article

class CreateArticleForm(forms.ModelForm):
    '''
    Form for creating a new article.
    '''
    class Meta:
        '''associate form with model from db'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']