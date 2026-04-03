# File: dadjokes/serializers.py
# Author: Kai Solter (ksolter@bu.edu), 4/2/2026 
# Description: Serializers for Dad Jokes app 

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''Serializer for Joke model'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributer', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    '''Serializer for Picture model'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributer', 'timestamp']

