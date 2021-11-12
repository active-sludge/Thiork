from django.db import models
from django.contrib.auth.models import User


class Vectis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username
