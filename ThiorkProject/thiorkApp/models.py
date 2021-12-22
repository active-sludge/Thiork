from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from location_field.models.plain import PlainLocationField


class Status(Enum):
    AVAILABLE = 'Available'
    PENDING = 'Pending'
    HANDSHAKEN = 'Handshaken'
    COMPLETED = 'Completed'


class Vectis(AbstractUser):
    pass
    credit = models.IntegerField(default=5)
    photo = models.ImageField(upload_to='profile_photos/%Y/%m/%d/', blank=True, default='ceyda.jpeg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username


class Servitium(models.Model):
    owner = models.ForeignKey(Vectis, on_delete=models.DO_NOTHING, related_name='servitium_owner')
    receiver = models.ManyToManyField(Vectis, through='Inquiry', through_fields=('servitium', 'receiver'))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)
    city = models.CharField(max_length=255, default='Istanbul')
    location = PlainLocationField(based_fields=['city'], zoom=5)
    credit = models.IntegerField()
    status = models.CharField(max_length=200, default='Available')
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



