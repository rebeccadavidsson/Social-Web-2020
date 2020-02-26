#!/usr/bin/python
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
# from django.contrib.auth.decorators import permission_required
from .helpers import get_profile
from .models import History, Profile

from subprocess import call


def index(request):
    """ Render main page when website is opened for the first time. """

    # Check if user is logged in
    if not request.user.is_authenticated:
        return render(request, "login.html")

    context = {}
    # TODO, waarschijnlijk users opvragen
    return render(request, 'mainpage.html', context)


def login_view(request):

    message = None

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If user already exists, redirect to index
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = "Invalid credentials."

        # TODO: Dit afmaken met registeren, model voor User aanmaken
        # return redirect("index")
    return render(request, "login.html", {"message": message})


def register_view(request):
    """Register new user"""

    if request.POST:
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        password_check = request.POST.get('password_confirm')

        # TODO: dit is veel mooier met JavaScript
        if not username or not password or not password_check:
            return render(request, "register.html", {"message": "Please fill in all fields."})

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"message": "This username is already taken."})

        # Create new user
        user = User.objects.create_user(
            username=username, password=password)
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        user = authenticate(request, username=username, password=password)

        # Create a new profile! :)
        new_user = Profile(user=user)
        new_user.save()

        if user is not None:
            login(request, user)
            return redirect("index")

    return render(request, "register.html")


def personal_view(request):
    """Render personal profile"""

    # get following user profiles
    following = Profile.objects.get(user=request.user).following.all()

    # list with usernames to exclude from 'to_follow', starts with own account
    to_exclude = [request.user.username]

    # get usernames of following users and append to list
    usernames = [person['username'] for person in following.values('username')]
    to_exclude += usernames

    # get all users
    all_users = User.objects.all()

    # show only users that you can follow
    to_follow = User.objects.exclude(username__in=to_exclude)

    # TODO: ingelogde user ophalen
    context = {
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": to_follow,
        "following": following
    }
    # TODO
    return render(request, 'personal.html', context)


def searchprofile(request, user):  # TODO, dit moet user_id worden
    """Go to someone else their profile page"""
    # TODO: deze functie en personal_view samenvoegen?
    context = {
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": User.objects.all()
    }

    return render(request, 'personal.html', context)


def follow(request, username):
    """Add follower to the profile of logged in user"""

    # get user profiles
    profile = Profile.objects.get(user=request.user)
    to_follow = Profile.objects.get(user__username=username)

    # TODO: if already following user, render message (in context? js?)

    # get user and add to following
    user_to_follow = User.objects.get(username=username)
    profile.following.add(user_to_follow)
    profile.save()

    return redirect("profile")


def unfollow(request, username):
    """Unfollow certain user"""

    # oke dit kan ook in follow functie maar lui en weet niet of dit perse handiger is!!
    profile = Profile.objects.get(user=request.user)
    to_unfollow = Profile.objects.get(user__username=username)
    profile.following.remove(to_unfollow.user)
    profile.save()

    return redirect("profile")


def settings_view(request):
    # TODO
    return redirect("profile")


def schedule_view(request):

    location = 5

    # Execute scraper
    # call(["node", "scraper/scraper.js"])

    context = {}
    # TODO
    return render(request, 'schedule.html', context)


def home_view(request):
    context = {}
    # TODO
    return render(request, 'home.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "login.html", {"message": "Logged out."})
    else:
        return render(request, "login.html", {"message": "You are already logged out."})
