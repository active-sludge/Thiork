from enum import Enum

from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Status(Enum):
    AVAILABLE = 'Available'
    PENDING = 'Pending'
    HANDSHAKEN = 'Handshaken'
    COMPLETED = 'Completed'


class Vectis(AbstractUser):
    pass
    credit = models.IntegerField(default=5)
    photo = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.username


class Servitium(models.Model):
    owner = models.ForeignKey(Vectis, on_delete=models.DO_NOTHING, related_name='servitium_owner')
    receiver = models.ManyToManyField(Vectis, through='Inquiry', through_fields=('servitium', 'receiver'))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(max_length=200)
    credit = models.IntegerField()
    status = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    servitium = models.ForeignKey(Servitium, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Vectis, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.servitium.title


class Eventum(models.Model):
    host = models.ForeignKey(Vectis, on_delete=models.DO_NOTHING, related_name='eventum_host')
    attendes = models.ManyToManyField(Vectis, through='Attendance', through_fields=('eventum', 'attendee'))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(max_length=200)
    credit = models.IntegerField()
    status = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    eventum = models.ForeignKey(Eventum, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Vectis, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.eventum.title



