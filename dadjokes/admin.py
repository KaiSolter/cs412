# File: dadjokes/admin.py
# Author: Kai Solter (ksolter@bu.edu), 4/2/2026
# Description: Admin configuration for dadjokes app
  
from django.contrib import admin

from .models import Joke, Picture

# Register your models here.    
admin.site.register(Joke)
admin.site.register(Picture)
