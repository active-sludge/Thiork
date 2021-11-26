from django.db import models
from django.contrib.auth.models import User


class Servitium(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='servitium_owner')
    receiver = models.ManyToManyField(User, through='Inquiry', through_fields=('servitium', 'receiver'))
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
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.servitium.title


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


class Vectis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.user.username
