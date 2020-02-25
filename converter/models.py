from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime



# NIKS WERKT AAAAAHHHH MAAR STRUCTUUR IS OKE??


# class Teacher(models.Model):
#     name = models.CharField(max_length=64)
#
#
# class ScheduleItem(models.Model):
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#     capacity = models.IntegerField(default=0)
#     full = models.BooleanField(default=False)
#     # participants = models.ManyToManyField(Profile, on_delete=models.PROTECT)
#
#
# class Course(models.Model):
#     name = models.CharField(max_length=64)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     scheduled_courses = models.ManyToManyField(ScheduleItem, on_delete=models.CASCADE)
#     price = models.DecimalField(decimal_places=2, max_digits=4)


class History(models.Model):
    # sportname = models.CharField(max_length=64)
    # teacher = models.CharField(max_length=64)  # Willen we dat dit ook een profiel wordt?
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    feedmessages = models.ManyToManyField(History, related_name="feedmessages")
    interests = models.CharField(max_length=64)  # Willen we hier ook een rating aan toevoegen?
    photo = models.ImageField(upload_to = "static/images", default = "images/logo.png")
