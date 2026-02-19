from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''文章模型'''
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''返回文章标题'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''返回文章详情页的URL'''
        return reverse('article', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    '''评论模型'''
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''返回评论作者和文章标题'''
        return f'{self.text}'