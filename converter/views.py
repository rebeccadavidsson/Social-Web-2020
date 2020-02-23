from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from .models import History, Profile


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
    Profile.objects.all().delete()

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

    # TODO: ingelogde user ophalen
    context = {
    "username": request.user,
    "firstname": request.user.first_name,
    "lastname": request.user.last_name,
    "users": User.objects.all()
    }
    # TODO
    return render(request, 'personal.html', context)


def searchprofile(request, user): #TODO, dit moet userid worden
    """Go to someone else their profile page"""

    context = {
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": User.objects.all()
    }

    return render(request, 'personal.html', context)


def follow(request, username):

    # Get user profile
    # TODO: DOET HET NOG NIET
    profile = Profile.objects.get(user=request.user)
    to_follow = Profile.objects.filter(user__username=username)

    profile.following.add(to_follow)
    profile.save()

    return redirect("profile")

def settings_view(request):
    context = {}
    # TODO
    return render(request, 'settings.html', context)

def schedule_view(request):
    context = {}
    # TODO
    return render(request, 'schedule.html', context)

def schedule_view(request):
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
