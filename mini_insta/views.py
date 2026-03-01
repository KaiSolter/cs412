# File: mini_insta/views.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: Views for mini_insta app 
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse

from mini_insta.forms import CreatePostForm, UpdateProfileForm
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
        return reverse('post', kwargs={'pk': self.object.pk})

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
        # image_url = self.request.POST.get('image_url')
        # if image_url:
        #     Photo.objects.create(
        #         post=self.object,
        #         image_url=image_url
        #     )
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(
                post=self.object,
                image_file=file
            )
        return response
    
class DeletePostView(DeleteView):
    '''
    Display html form to user and process submission deleting the post
    '''
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    
    def get_context_data(self, **kwargs):
        ''' Add the profile to the context so we can redirect to the correct profile page after deleting'''
        context = super().get_context_data(**kwargs)
        post = self.object
        profile = post.profile
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        '''After successfully deleting a post, redirect to the profile page'''
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk}) 
    
class UpdatePostView(UpdateView):
    '''
    Display html form to user and process submission updating the post
    '''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/update_post_form.html"
    
    def get_context_data(self, **kwargs):
        ''' Add the profile to the context so we can redirect to the correct profile page after updating'''
        context = super().get_context_data(**kwargs)
        post = self.object
        profile = post.profile
        context['profile'] = profile
        return context

    def get_success_url(self):
        '''After successfully updating a post, redirect to the profile page'''
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk}) 
    
class UpdateProfileView(UpdateView):
    '''
    Display html form to user and process submission storing the updated profile data
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    

class ShowFollowersDetailView(DetailView):
    '''
    Display a list of followers for a profile
    '''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = 'profile'
    
class ShowFollowingDetailView(DetailView):
    '''
    Display a list of profiles that a profile is following
    '''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = 'profile'
    
class PostFeedListView(ListView):
    '''
    Display a post feed for a profile (posts from profiles this profile is following)
    '''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = 'feed'
    
    def get_context_data(self, **kwargs):
        ''' Add the relevant info to the context'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['feed_posts'] = profile.get_post_feed()
        context['profile'] = profile
        return context