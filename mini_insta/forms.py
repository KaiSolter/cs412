# File: mini_insta/forms.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026
# Description: Forms for mini_insta app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''
    Form for creating a new post.
    '''    
    class Meta:
        '''associate form with model'''
        model = Post
        fields = ['caption']