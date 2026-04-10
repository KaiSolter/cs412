# File: mini_insta/serializers.py
# Author: Kai Solter (ksolter@bu.edu), 4/7/2026 
# Description: Serializers for Mini Insta app 

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer for the Profile model'''
    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    '''Serializer for the Post model'''
    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp']
        read_only_fields = ['id', 'profile', 'timestamp']
        
class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer for the Photo model'''
    class Meta:
        model = Photo
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for the Comment model'''
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    '''Serializer for the Like model'''
    class Meta:
        model = Like
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    '''Serializer for the Follow model'''
    class Meta:
        model = Follow
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, trim_whitespace=False)
