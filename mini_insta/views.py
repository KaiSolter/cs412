from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Profile
# Create your views here.
class ProfileListView(ListView):
    '''
    Display all profiles
    '''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'
    
    
class ProfileDetailView(DetailView):
    '''
    Display a single profile
    '''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'
    
class PostDetailView(DetailView):
    '''
    Display a single post
    '''
    model = Post
    template_name = "mini_insta/post.html"
    context_object_name = 'post'