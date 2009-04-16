from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to='photos/', blank=True)
    cropped = models.ImageField(upload_to='cropped/', blank=True)

