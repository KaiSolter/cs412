# File: dadjokes/views.py
# Author: Kai Solter (ksolter@bu.edu), 4/2/2026 
# Description: Views for Dad Jokes app 

import random
from django.http import Http404
from django.views.generic import ListView, DetailView

from  .models import Joke, Picture

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
    template_name = 'dadjokes/random.html'
    context_object_name = 'joke'

    def get_object(self, queryset=None):
        queryset = queryset or Joke.objects.all()
        if not queryset.exists():
            raise Http404('No jokes available.')
        return random.choice(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pictures = Picture.objects.all()
        if pictures:
            context['picture'] = random.choice(pictures)
        else:
            context['picture'] = None
        return context
    
    