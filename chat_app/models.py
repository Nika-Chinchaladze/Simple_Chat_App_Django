from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from json import dumps, loads


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1500, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def generate_room_url(self):
        return reverse("room", args=[self.slug])

    def __str__(self):
        return f"{self.name}"


class RoomUsers(models.Model):
    username_room = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.username_room}"


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value} {self.date} {self.user} {self.room}"
