from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse

from mini_insta.forms import CreatePostForm
from .models import *
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
    
class CreatePostView(CreateView):
    '''
    Display html form to user and process submission storing the new data object
    '''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post.html"
    
    def get_success_url(self):
        '''After successfully creating a post, redirect to the post page
        '''
        pk = self.kwargs['pk']
        return reverse('post', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        ''' Add the profile to the context so we can associate the new post with the correct profile'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Associate the new post with the correct profile before saving'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        
        # Save the post first
        response = super().form_valid(form)
        
        # Now create the Photo object with the image_url from the form
        image_url = self.request.POST.get('image_url')
        if image_url:
            Photo.objects.create(
                post=self.object,
                image_url=image_url
            )
        
        return response