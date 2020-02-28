from django.contrib import admin
from .models import ScheduleItem, Profile, Rating

admin.site.register(Profile)
admin.site.register(ScheduleItem)
admin.site.register(Rating)
