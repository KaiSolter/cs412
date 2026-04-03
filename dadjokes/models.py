# File: mini_insta/admin.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026
# Description: Admin configuration for mini_insta app

from django.db import models

# Create your models here.
class Joke(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    contributer = models.TextField()
    def __str__(self):
        return self.text
    
class Picture(models.Model):
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    contributer = models.TextField()
    def __str__(self):
        return self.image_url