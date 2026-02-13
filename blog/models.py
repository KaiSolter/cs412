from django.db import models

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