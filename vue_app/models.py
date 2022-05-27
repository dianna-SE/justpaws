from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# MUST MAKE MIGRATIONS IF MODELS ARE EDITED #
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to='profile_images', default = 'paw-profile-default.jpg')
    location = models.CharField(max_length = 50, blank = True)
    firstname = models.CharField(max_length = 20, blank = True)
    lastname = models.CharField(max_length = 20, blank = True)

    # NAMING THE MODEL #
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'post_images')
    caption = models.TextField(max_length = 80)
    created_at = models.DateTimeField(default = datetime.now)
    no_of_downloaded = models.IntegerField(default = 0)

    # NEW
    file_name = models.TextField(max_length = 20, blank = True)
    course_name = models.TextField(max_length = 20, blank = True)

    def __str__(self):
        return self.user





class FollowersCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)

    def __str__(self):
        return self.user


class PostUser(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    user = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'post_images')
    profileimg = models.ImageField(upload_to='profile_images', default = 'paw-profile-default.jpg')
    filename = models.TextField(max_length = 20)
    caption = models.TextField(max_length = 50)
    created_at = models.DateTimeField(default = datetime.now)
    no_of_downloaded = models.IntegerField(default = 0)

    def __str__(self):
        return self.user