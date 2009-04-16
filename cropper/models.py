from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to='photos/', blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

