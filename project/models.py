# File: project/models.py
# Author: Kai Solter (ksolter@bu.edu), 4/19/2026 
# Description: models for final project app 

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''
    Profile Model
    '''
    username = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_articles = models.ManyToManyField('Article', blank=True)

class Organization(models.Model):
    '''
    Organization Model
    '''
    name = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    description = models.TextField(blank=True)
    bias = models.TextField(blank=True)
    independent = models.BooleanField(default=False)

class Topic(models.Model):
    '''
    Topic Model
    '''
    topic = models.TextField(blank=True)
    description = models.TextField(blank=True)

class Article(models.Model):
    '''
    Article Model
    '''
    title = models.TextField(blank=True)
    url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    full_text = models.TextField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
class FollowOrganization(models.Model):
    '''
    Follow Model
    '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='following')
    
class FollowTopic(models.Model):
    '''
    Follow Model
    '''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_topic')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='following_topic')
    