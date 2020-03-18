from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', null=True, blank=True)
    interests = models.CharField(max_length=64, null=True, blank=True)  # Willen we hier ook een rating aan toevoegen?
    photo = models.ImageField(upload_to = "images", default = "images/logo.png")

    def __str__(self):
        return f'{self.user}'


class ScheduleItem(models.Model):
    teacher = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    start = models.CharField(max_length=64)
    end = models.CharField(max_length=64)
    date = models.CharField(max_length=64)
    participants = models.ManyToManyField(Profile, related_name="participants")
    likes = models.IntegerField(default=0)
    hearts = models.IntegerField(default=0)

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

    def __str__(self):
        return f'{self.name} - {self.teacher} - {self.start}'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = IntegerField(
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    comment = models.CharField(max_length=300)
    # event_id = models.IntegerField(default=0)
    event = models.ForeignKey(ScheduleItem, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.comment} - {self.rating}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


# class Course(models.Model):
#     name = models.CharField(max_length=64)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     scheduled_courses = models.ManyToManyField(ScheduleItem, on_delete=models.CASCADE)
#     price = models.DecimalField(decimal_places=2, max_digits=4)
