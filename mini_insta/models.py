# File: mini_insta/templates/mini_insta/models.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: Models for mini_insta app 
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''
    Profile Model
    '''
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mini_insta_profiles')
    
    def get_all_posts(self):
        ''''get all posts associated with this profile'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url (self):
        '''get the url for this profile'''
        return f'/mini_insta/profile/{self.pk}'
    
    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        return f' user: {self.username}, with display name {self.display_name}'
    
    def get_followers(self):
        '''get all followers of this profile'''
        followers = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in followers]
    
    def get_following(self):
        '''get all profiles this profile is following'''
        following = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in following]
    
    def get_num_followers(self):
        '''get the number of followers for this profile'''
        return len(self.get_followers())
    
    def get_num_following(self):
        '''get the number of profiles this profile is following'''
        return len(self.get_following())
    
    def get_post_feed(self):
        '''get the post feed for this profile (posts from profiles this profile is following)'''
        following_profiles = self.get_following()
        feed_posts = []
        for profile in following_profiles:
            feed_posts.extend(profile.get_all_posts())
        feed_posts.sort(key=lambda post: post.timestamp, reverse=True)
        return feed_posts
    
class Post(models.Model):
    '''
    Post Model
    '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_all_photos(self):
        '''get all photos associated with this post'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_all_comments(self):
        '''get all comments associated with this post'''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        '''get all likes associated with this post'''
        likes = Like.objects.filter(post=self)
        return likes
    
    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        return f'{self.caption}'

class Photo(models.Model):
    '''
    Photo Model
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def get_image_url(self):
        '''get the image url for this photo'''
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url

    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        image = self.image_file.url if self.image_file else self.image_url
        return f'Image: {image} for post: {self.post.caption}'
    
class Follow(models.Model):
    '''
    Follow Model to store relationships between profiles
    '''
    profile = models.ForeignKey(Profile, related_name='profile', on_delete=models.CASCADE)
    follower_profile = models.ForeignKey(Profile, related_name='follower_profile', on_delete=models.CASCADE)
    
    def __str__(self):
        ''' Docstring for __str__'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'
    

class Comment(models.Model):
    '''
    Comment Model to store comments on posts
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)
    
    def __str__(self):
        ''' Docstring for __str__'''
        return f'{self.text}'
    
class Like(models.Model):
    '''
    Like Model to store likes on posts
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        ''' Docstring for __str__'''
        return f'{self.profile.display_name} likes {self.post.caption}'