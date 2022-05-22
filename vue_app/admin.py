from django.contrib import admin
from .models import Profile, Post

# MANAGES MODULES IN ADMIN PANEL #
admin.site.register(Profile)
admin.site.register(Post)