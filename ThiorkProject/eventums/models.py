from django.db import models
from django.contrib.auth.models import User


class Eventum(models.Model):
    host = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='eventum_host')
    attendes = models.ManyToManyField(User, through='Attendance', through_fields=('eventum', 'attendee'))
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
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.eventum.title
