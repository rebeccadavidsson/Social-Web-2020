#!/usr/bin/python
import os
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from subprocess import call

# from django.contrib.auth.decorators import permission_required
from .models import Profile, ScheduleItem, Rating
from .forms import ProfileForm
from .scrape import scrape_item
from .helpers import convertdate, refreshschedule


def index(request):
    """ Render main page when website is opened for the first time. """

    # Check if user is logged in
    if not request.user.is_authenticated or request.user.username == "admin":
        return render(request, "login.html")

    # Get user profile and the people this user is following
    profile = Profile.objects.get(user=request.user)
    followers = profile.following.all()

    # Get events from other followers
    empt = []
    for follower in followers:
        to_follow = Profile.objects.get(user__username=follower.username)
        item = ScheduleItem.objects.filter(participants=to_follow).all()
        if item:
            empt.append(item)

    # Index into query if the people you follow also have events
    if empt:
        empt = empt[0]

    events_user = ScheduleItem.objects.filter(participants=profile).all()

    ratings_user = Rating.objects.all()

    rated_events = Rating.objects.filter(user=request.user)


    # user_ratings = []
    # for ratings in events_user:
    #     user_ratings.append(Rating.objects.filter(event=ratings))
    #
    # if user_ratings:
    #     user_ratings = user_ratings[0]


    # Filter events for user
    context = {
        "profile": profile,
        "events": ScheduleItem.objects.all(),
        "events_user": events_user,
        "event_followers": empt,
        "ratings_user": ratings_user,
        "rated_events": rated_events,
        "checker": False
    }

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
    profile = Profile.objects.get(user=request.user)
    following = profile.following.all()

    # list with usernames to exclude from 'to_follow', starts with own account
    to_exclude = [request.user.username]

    # get usernames of following users and append to list
    usernames = [person['username'] for person in following.values('username')]
    to_exclude += usernames

    # get all users
    all_users = User.objects.all()

    # show only users that you can follow
    to_follow = User.objects.exclude(username__in=to_exclude)

    # get all events from this user
    events_user = ScheduleItem.objects.filter(participants=profile).all()

    # get all rating from this user
    ratings = Rating.objects.filter(user=request.user).all()

    context = {
        "profile": profile,
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "users": to_follow,
        "following": following,
        "events_user": events_user,
        "ratings": ratings,
        "n": [1,2,3,4,5]
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


def settings_view(request,pk):
    """
    Let user edit their profile.
    """

    # get user's profile model
    profile = Profile.objects.get(user=request.user)

    # if user wants to edit profile
    if request.method == "POST":

        # get form and validate form
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            form.photo = request.POST.get("photo", False)
            # file_type = form.photo.url.split('.')[-1].lower()
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    context = {
        "user": request.user,
        "form": form,
        "profile": profile
    }
    return render(request, "settings.html", context)




def schedule_view(request):

    # Check if schedule was already refreshed this day TODO
    # refreshschedule()

    # get user's profile model
    profile = Profile.objects.get(user=request.user)

    context = {
        "profile": profile
    }

    return render(request, 'schedule.html', context)


def addschedule(request):
    """
    Create schedule item.
    default location = universum (TODO!)
    """

    data = scrape_item(request.POST.get("data"))

    # Get user to add to participants
    profile = Profile.objects.get(user=request.user)

    # Check if this item already exists before creating a new one
    # TODO: Sam kan dit mooier? ;)
    try:
        check = ScheduleItem.objects.filter(teacher=data["teacher"],
                                            name=data["sort"],
                                            start=data["start"],
                                            end=data["end"]).first()
    except:
        check = None

    # Add profile to already existing item, else create new item
    if check:
        check.participants.add(profile)
    else:
        # Create new item
        item = ScheduleItem(teacher=data["teacher"],
                            name=data["sort"],
                            start=data["start"],
                            end=data["end"],
                            date=convertdate(data["start"]))
        item.save()
        item.participants.add(profile)

    # TODO wat moet hier?
    return HttpResponse("test")


def review(request, event_id):
    """Save user's review of a training session."""

    # TODO check if comment and rating is entered --> javascript :)
    review = request.POST["comment"]
    rating = request.POST["rating"]

    print(review, rating, event_id, "HSHKFJHSKJ")
    event = ScheduleItem.objects.get(id=event_id)
    # Rating.objects.all().delete()

    # check if user already left rating, ask if they want to rerate the class
    # if Rating.objects.filter(user=request.user, event=event).exists():
    #     return render(request, "/", {"message": "You already left a rating for this course."})

    # create new rating
    new_rating = Rating(user=request.user,
                        comment=review,
                        rating=int(rating),
                        event=event)
    new_rating.save()

    return redirect("/")


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
