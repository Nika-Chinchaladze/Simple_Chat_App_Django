from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1500, null=True)

    def generate_room_url(self):
        return reverse("room", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value} {self.date} {self.user} {self.room}"
