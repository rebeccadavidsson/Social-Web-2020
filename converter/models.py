from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Teacher(models.Model):
    name = models.CharField(max_length=64)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    # feedmessages = models.ManyToManyField(History, related_name="feedmessages")
    interests = models.CharField(max_length=64)  # Willen we hier ook een rating aan toevoegen?
    photo = models.ImageField(upload_to = "static/images", default = "images/logo.png")


class ScheduleItem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    participants = models.ManyToManyField(Profile, related_name="participants")

    locations = [
        ("universum", "Universum"),
        ("asc", "ASC"),
        ("amstel", "Amstelcampus"),
        ("crea", "CREA"),
        ("clubwest", "ClubWest"),
    ]
    location = models.CharField(
        max_length=64,
        choices=locations,
        default="universum",
    )


class History(models.Model):
    rating = models.IntegerField(default=0)
    item = models.ForeignKey(ScheduleItem, on_delete=models.CASCADE)
