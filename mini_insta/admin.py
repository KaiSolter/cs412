# File: mini_insta/admin.py
# Author: Kai Solter (ksolter@bu.edu), 2/13/2026
# Description: Admin configuration for mini_insta app

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
