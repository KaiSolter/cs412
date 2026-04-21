from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Organization)
admin.site.register(Topic)
admin.site.register(Article)
admin.site.register(FollowOrganization)
admin.site.register(FollowTopic)
