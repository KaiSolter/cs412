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
        
class UpdateProfileForm(forms.ModelForm):
    '''
    Form for updating a profile.
    '''    
    class Meta:
        '''associate form with model'''
        model = Profile
        # Don't allow user to update username or join date
        fields = ['display_name', 'profile_image_url', 'bio_text']