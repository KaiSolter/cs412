# File: project/forms.py
# Author: Kai Solter (ksolter@bu.edu), 4/30/2026
# Description: Forms for the project app

from django import forms
from .models import Profile


class ArticleSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search articles...', 'autofocus': True}),
    )
    include_external = forms.BooleanField(
        label='Include external results (NewsAPI)',
        required=False,
        initial=True,
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a short bio...'}),
        }
