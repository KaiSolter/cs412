# File: dadjokes/views.py
# Author: Kai Solter (ksolter@bu.edu), 4/2/2026 
# Description: Views for Dad Jokes app 

import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.dadjokes.models import Joke, Picture

# Create your views here.
class JokeListView(ListView):
    model = Joke
    template_name = 'dadjokes/alljokes.html'
    context_object_name = 'jokes'
    
class PictureListView(ListView):
    model = Picture
    template_name = 'dadjokes/allpictures.html'
    context_object_name = 'pictures'
    
class JokeDetailView(DetailView):
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'
    
class PictureDetailView(DetailView):
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'
    
class RandomJokeView(DetailView):
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'
    
    def get_object(self, queryset=None):
        jokes = Joke.objects.all()
        if jokes:
            return random.choice(jokes)
        return None
    
    