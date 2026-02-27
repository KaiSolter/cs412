# File: mini_insta/templates/mini_insta/models.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026 
# Description: Models for mini_insta app 
from django.db import models

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
    
    def get_all_posts(self):
        ''''get all posts associated with this profile'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        return f' user: {self.username}, with display name {self.display_name}'
    
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
    