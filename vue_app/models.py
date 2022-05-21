from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# MUST MAKE MIGRATIONS IF MODELS ARE EDITED #
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to='profile_images', default = 'paw-profile-default.jpg')
    location = models.CharField(max_length = 50, blank = True)

    # NAMING THE MODEL #
    def __str__(self):
        return self.user.username