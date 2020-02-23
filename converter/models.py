from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class History(models.Model):
    sportname = models.CharField(max_length=64)
    teacher = models.CharField(max_length=64)  # Willen we dat dit ook een profiel wordt?
    rating = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    feedmessages = models.ManyToManyField(History, related_name="feedmessages")
    interests = models.CharField(max_length=64)  # Willen we hier ook een rating aan toevoegen?
