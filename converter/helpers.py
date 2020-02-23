from django.contrib.auth.models import User
from .models import History, Profile


def get_profile(request):
    return Profile.objects.get(user=request.user)
