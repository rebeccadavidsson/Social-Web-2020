from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class History(models.Model):
    # sportname = models.CharField(max_length=64)
    # teacher = models.CharField(max_length=64)  # Willen we dat dit ook een profiel wordt?
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)

    date = models.DateField(default=timezone.now)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = IntegerField(
        default=3,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    feedmessages = models.ManyToManyField(History, related_name="feedmessages")
    interests = models.CharField(max_length=64)  # Willen we hier ook een rating aan toevoegen?
    photo = models.ImageField(upload_to = "static/images", default = "images/logo.png")


class Teacher(models.Model):
    name = models.CharField(max_length=64)


class ScheduleItem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    participants = models.ManyToManyField(Profile, related_name="participants")
    rating = models.ManyToManyField(Rating, related_name="ratings")

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


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


#
#
# class Course(models.Model):
#     name = models.CharField(max_length=64)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     scheduled_courses = models.ManyToManyField(ScheduleItem, on_delete=models.CASCADE)
#     price = models.DecimalField(decimal_places=2, max_digits=4)
