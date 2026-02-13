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
    
    def __str__(self):
        '''
        Docstring for __str__
        
        :param self: Description
        '''
        return f' user: {self.username}, with display name {self.display_name}'