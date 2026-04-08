# File: mini_insta/views.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: Views for mini_insta app 
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from rest_framework import generics

from mini_insta.forms import CreatePostForm, CreateProfileForm, UpdateProfileForm
from .models import *
from .serializers import *
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

    def get_context_data(self, **kwargs):
        '''Add follow state for the logged-in user when viewing another profile.'''
        context = super().get_context_data(**kwargs)
        is_following = False

        # Check if this is a different profile and if the logged in user is already a follower or not
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            other_profile = self.object
            if my_profile != other_profile:
                is_following = Follow.objects.filter(
                    follower_profile=my_profile,
                    profile=other_profile,
                ).exists()

        context['is_following'] = is_following
        return context

class ProfileSelfDetailView(LoginRequiredMixin, DetailView):
    '''
    Display the logged-in user's own profile
    '''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'
    
    def get_object(self):
        '''Get the profile object for the logged-in user'''
        return Profile.objects.get(user=self.request.user)


class FollowView(LoginRequiredMixin, View):
    '''Create a follow relationship from the logged-in user to the target profile.'''

    def post(self, request, *args, **kwargs):
        target_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = Profile.objects.get(user=request.user)

        if target_profile == my_profile:
            return redirect('profile', pk=target_profile.pk)

        existing = Follow.objects.filter(
            follower_profile=my_profile,
            profile=target_profile,
        )

        if not existing.exists():
            Follow.objects.create(
                follower_profile=my_profile,
                profile=target_profile,
            )

        return redirect('profile', pk=target_profile.pk)


class DeleteFollowView(LoginRequiredMixin, View):
    '''Delete the follow relationship from the logged-in user to the target profile (Allows unfollow)'''

    def post(self, request, *args, **kwargs):
        target_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = Profile.objects.get(user=request.user)

        Follow.objects.filter(
            follower_profile=my_profile,
            profile=target_profile,
        ).delete()

        return redirect('profile', pk=target_profile.pk)
    
class PostDetailView(DetailView):
    '''
    Display a single post
    '''
    model = Post
    template_name = "mini_insta/post.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Add like state for the logged-in user when viewing a post (So we can handle likes)'''
        context = super().get_context_data(**kwargs)
        is_liked = False

        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            post = self.object
            if my_profile != post.profile:
                is_liked = Like.objects.filter(
                    profile=my_profile,
                    post=post,
                ).exists()

        context['is_liked'] = is_liked
        return context


class LikePostView(LoginRequiredMixin, View):
    '''Create a like from the logged-in user for the target post.'''
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = Profile.objects.get(user=request.user)

        # Disallow liking your own post.
        if post.profile == my_profile:
            return redirect('post', pk=post.pk)

        existing = Like.objects.filter(profile=my_profile, post=post)
        if not existing.exists():
            Like.objects.create(profile=my_profile, post=post)

        return redirect('post', pk=post.pk)


class UnlikePostView(LoginRequiredMixin, View):
    '''Delete the logged-in user's like for the target post.'''

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = Profile.objects.get(user=request.user)

        Like.objects.filter(profile=my_profile, post=post).delete()
        return redirect('post', pk=post.pk)
    
class CreatePostView(LoginRequiredMixin, CreateView):
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
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Associate the new post with the correct profile before saving'''
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        
        user = self.request.user
        form.instance.user = user
        
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
    
class DeletePostView(LoginRequiredMixin, DeleteView):
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
    
    def form_valid(self, form):
        '''Associate the post with the correct profile before deleting'''
     
        user = self.request.user
        if self.object.profile.user != user:
            raise PermissionDenied("You can only delete your own post.")
        form.instance.user = user
        return super().form_valid(form)
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
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
    
    def form_valid(self, form):
        '''Associate the post with the correct profile before updating'''
        user = self.request.user
        if self.object.profile.user != user:
            raise PermissionDenied("You can only edit your own post.")
        form.instance.user = user
        return super().form_valid(form)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''
    Display html form to user and process submission storing the updated profile data
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    
    def get_object(self):
        '''Get the profile object for the logged-in user'''
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        '''Associate the profile with the correct user before updating'''
        user = self.request.user
        if self.object.user != user:
            raise PermissionDenied("You can only edit your own profile.")
        form.instance.user = user
        return super().form_valid(form)
    

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
    
class PostFeedListView(LoginRequiredMixin, ListView):
    '''
    Display a post feed for a profile (posts from profiles this profile is following)
    '''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = 'feed'
    
    def get_context_data(self, **kwargs):
        ''' Add the relevant info to the context'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['feed_posts'] = profile.get_post_feed()
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''user must be logged in to view feed'''
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
class SearchView(LoginRequiredMixin, ListView):
    '''Display search results for profiles and posts'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def form_valid(self, form):
        '''user must be logged in to view feed'''
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        '''Check if query parameter exists. If not, show search form.'''
        query = request.GET.get('q')
        if not query:
            profile = Profile.objects.get(user=self.request.user)
            context = {'profile': profile}
            return render(request, 'mini_insta/search.html', context)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Get all posts that match the query'''
        query = self.request.GET.get('q')
        return Post.objects.filter(caption__icontains=query)
    
    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context'''
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        profile = Profile.objects.get(user=self.request.user)
        
        # Get profiles that match the query (searching both username and display name)
        profiles = Profile.objects.filter(
            Q(username__icontains=query) | Q(display_name__icontains=query)
        )
        
        context['profile'] = profile
        context['query'] = query
        context['profiles'] = profiles
        return context
    
class CreateProfileView(CreateView):
    ''''Display html form to user and process submission storing the new profile data
    '''
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile.html"
    
    def get_context_data(self, **kwargs):
        ''' Add the profile to the context so we can associate the new profile with the correct user'''
        context = super().get_context_data(**kwargs)
        if 'user_creation_form' not in context:
            if self.request.method == 'POST':
                context['user_creation_form'] = UserCreationForm(self.request.POST)
            else:
                context['user_creation_form'] = UserCreationForm()
        return context
    
    def get_success_url(self):
        '''After successfully creating a profile, redirect to the profile page'''
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        '''Associate the new profile with the correct user before saving'''
        UCF = UserCreationForm(self.request.POST)
        if UCF.is_valid():
            user = UCF.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            form.instance.join_date = timezone.now()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_creation_form=UCF))
        
class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        profile_pk = self.kwargs.get('profile_pk')  # from URL
        profile = get_object_or_404(Profile, pk=profile_pk)
        return Post.objects.filter(profile=profile).order_by('-timestamp')

    def perform_create(self, serializer):
        profile_pk = self.kwargs.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        serializer.save(profile=profile)
        
class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PhotoListAPIView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        return Photo.objects.filter(post=post).order_by('-timestamp')

class PhotoCreateAPIView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PostFeedListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        profile_pk = self.kwargs.get('profile_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        following_profiles = profile.get_following()
        return Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
    