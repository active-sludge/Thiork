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