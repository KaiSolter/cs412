from tokenize import Comment

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
        ''''返回用户的所有帖子'''
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
        '''返回帖子的所有照片'''
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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''
        Docstring for __str__
        :param self: Description
        '''
        return f'Image: {self.image_url} for post: {self.post.caption}'
    