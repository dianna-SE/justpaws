from django.contrib import admin
from .models import Profile, Post, FollowersCount

# MANAGES MODULES IN ADMIN PANEL #
admin.site.register(Profile)
admin.site.register(Post) 
admin.site.register(FollowersCount)