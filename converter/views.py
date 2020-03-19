#!/usr/bin/python
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import collections
# from subprocess import call

# from django.contrib.auth.decorators import permission_required
from .models import Profile, ScheduleItem, Rating
from .forms import ProfileForm, ProfileDeleteForm, RatingDeleteForm
from .scrape import scrape_item
from .helpers import convertdate, refreshschedule, geteventday


# def index(request):
#     """ Render main page when website is opened for the first time. """
#
#     # Check if user is logged in
#     if not request.user.is_authenticated or request.user.username == "admin":
#         return render(request, "login.html")
#
#     # Get user profile and the people this user is following
#     profile = Profile.objects.get(user=request.user)
#     followers = profile.following.all()
#
#     # Get events from other followers
#     empt, followersnames = [], []
#
#     for follower in followers:
#         to_follow = Profile.objects.get(user__username=follower.username)
#         item = ScheduleItem.objects.filter(participants=to_follow).exclude(participants=profile).all().order_by('-start')
#         if item:
#             empt.append(item.all())
#
#     empt2 = empt
#
#     for follower in profile.following.all():
#         followersnames.append(follower.first_name)
#
#     tempempt = []
#     # Index into query if the people you follow also have events
#     if empt:
#         empt.append(ScheduleItem.objects.filter(participants=profile).all().order_by('-start'))
#         for i in empt:
#             tempempt.append(i[0])
#         empt2 = empt2[0]
#     empt = tempempt
#     events = ScheduleItem.objects.all().order_by('-start')
#
#     previousevents, futurevents = geteventday(events)
#
#     # Get events for logged in user
#     events_user = ScheduleItem.objects.filter(participants=profile).all()
#
#     to_exclude = []
#     # Exclude double events of friends
#     for item in events_user:
#         if item in empt:
#             to_exclude.append(item.id)
#
#     events_user = events_user.exclude(id__in=to_exclude)
#
#     print(empt, "HAMBURGER")
#
#     # Filter events for user
#     context = {
#         "profile": profile,
#         "events": ScheduleItem.objects.all().order_by('-start'),
#         "ownevents": ScheduleItem.objects.filter(participants=profile).all().order_by('-start'),
#         "events_aftertoday": futurevents,
#         "events_beforetoday": previousevents,
#         "events_user": events_user,
#         "event_followers_includingown": empt,
#         "event_followers": empt2,
#         "followersnames": followersnames,
#         "ratings_user": Rating.objects.all(),
#         "rated_events": Rating.objects.filter(user=request.user),
#     }
#     # for event_blijkbaar in empt2:
#     #     if event_blijkbaar in ScheduleItem.objects.filter(participants=profile).all():
#     #         print("EVENT: ", event_blijkbaar)
#
#     return render(request, 'mainpage.html', context)

def index(request):
    """ Render main page when website is opened for the first time. """

    # Check if user is logged in
    if not request.user.is_authenticated or request.user.username == "admin":
        return render(request, "login.html")

    # Get user profile and the people this user is following
    profile = Profile.objects.get(user=request.user)
    followers = profile.following.all()

    # Get events from other followers
    empt, empt1, followersnames, temp = [], [], [], []

    for follower in followers:
        to_follow = Profile.objects.get(user__username=follower.username)
        # item = ScheduleItem.objects.filter(participants=to_follow).exclude(participants=profile).all().order_by('-start')
        items = ScheduleItem.objects.filter(participants=to_follow).all().order_by('-start')
        if items:

            for item in items:

                temp.append(ScheduleItem.objects.get(id=item.id))
            empt.append(item)

        item1 = ScheduleItem.objects.filter(participants=to_follow).exclude(participants=profile).all().order_by('-start')
        if item1:
            empt1.append(item1)

    empt2 = empt


    for follower in profile.following.all():
        followersnames.append(follower.first_name)

    # Index into query if the people you follow also have events
    if empt:
        empt = empt[0]
        empt2 = empt2[0]

    if empt1:
        empt1 = empt1[0]

    events = ScheduleItem.objects.all().order_by('-start')

    previousevents, futurevents = geteventday(events)


    # Filter events for user
    context = {
        "profile": profile,
        "events": ScheduleItem.objects.all().order_by('-start'),
        "ownevents": ScheduleItem.objects.filter(participants=profile).all().order_by('-start'),
        "events_aftertoday": futurevents,
        "events_beforetoday": previousevents,
        "events_user":  ScheduleItem.objects.filter(participants=profile).all(),
        "event_followers_includingown": temp,
        "emp1": empt1,
        "event_followers": empt2,
        "followersnames": followersnames,
        "ratings_user": Rating.objects.all(),
        "rated_events": Rating.objects.filter(user=request.user),
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
    following_profiles = []

    for usr in following:
        following_profiles.append(Profile.objects.filter(user=usr))

    # get all the people that is following this person
    allprofiles = Profile.objects.all()
    followers_for_this_person = []
    for profile in allprofiles:
        if request.user in profile.following.all():
            followers_for_this_person.append(profile)

    # list with usernames to exclude from 'to_follow', starts with own account
    to_exclude = [request.user.username]

    # get usernames of following users and append to list
    usernames = [person['username'] for person in following.values('username')]
    to_exclude += usernames

    # show only users that you can follow
    to_follow = User.objects.exclude(username__in=to_exclude)
    profiles_to_follow = Profile.objects.exclude(user__username__in=to_exclude)
    searchprofiles = Profile.objects.exclude(user__username__in=[profile])
    # get all events from this user
    events_user = ScheduleItem.objects.filter(participants=profile).all().order_by("-start")

    # get all rating from this user
    ratings = Rating.objects.filter(user=request.user).all()

    events = ScheduleItem.objects.all().order_by("-start")
    # Seperate previous and future events
    previousevents, futurevents = geteventday(events)

    context = {
        "profile": profile,
        "username": request.user,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name,
        "following_profiles": following_profiles,
        "users": to_follow,
        "followers_for_this_person": followers_for_this_person,
        "profiles_to_follow": profiles_to_follow,
        "searchprofiles": searchprofiles,
        "following": following,
        "events_user": events_user,
        "previousevents": previousevents,
        "ratings": ratings,
        "n": [1, 2, 3, 4, 5]
    }

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


def settings_view(request, pk):
    """
    Let user edit their profile.
    """

    # get user's profile model
    profile = Profile.objects.get(user=request.user)

    # if user wants to edit profile
    if request.method == "POST":

        # get form and validate form
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print("----------------------------",form)
        print("))--", request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.photo = request.POST.get("photo")
            # file_type = form.photo.url.split('.')[-1].lower()
            form.save()

            # profile.photo =
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
    print(request.POST.get("data"), "PIRNITNR")
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


def add(request, event_id):
    """
    Add a new event_id from the mainpage by clicking on
    a review or past class from someone else.
    """

    # Get user to add to participants
    profile = Profile.objects.get(user=request.user)

    # Select event from event_id
    item = ScheduleItem.objects.filter(id=event_id).first()
    item.participants.add(profile)

    return redirect('/')


def deleteevent(request, event_id):

    # Get user to add to participants
    profile = Profile.objects.get(user=request.user)

    # Select event from event_id
    item = ScheduleItem.objects.filter(id=event_id).first()
    item.participants.remove(profile)

    return redirect("/")

def review(request, event_id):
    """Save user's review of a training session."""

    # TODO check if comment and rating is entered --> javascript :)
    review = request.POST["comment"]
    try:
        rating = int(request.POST["rating"])
    except:
        rating = 0

    event = ScheduleItem.objects.get(id=event_id)

    # check if user already left rating, ask if they want to rerate the class
    event_to_rate = Rating.objects.filter(user=request.user, event=event).first()

    if event_to_rate:
        event_to_rate.comment = review
        event_to_rate.rating = rating
        event_to_rate.save()

    else:
        # create new rating
        new_rating = Rating(user=request.user,
                            comment=review,
                            rating=rating,
                            event=event)
        new_rating.save()

    return redirect("/")


def home_view(request):
    context = {}
    # TODO
    return render(request, 'home.html', context)


def delete_rating(request, pk):
    rating = get_object_or_404(Rating, pk=pk)
    if rating.user == request.user and request.method == "POST":
        form = RatingDeleteForm(request.POST, instance=rating)
        if form.is_valid():
            rating.delete()
            return redirect("index")
    else:
        form = PostDeleteForm(instance=rating)

    return redirect("index")

def delete_profile(request, username):

    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = ProfileDeleteForm(request.POST, instance=user)
        if form.is_valid():
            user.delete()
            return redirect("login")
    else:
        form = PostDeleteForm(instance=form)

    return redirect("index")


def like(request, event_id):
    event = ScheduleItem.objects.filter(id=event_id).first()
    event.likes += 1
    event.save()
    return redirect("/")

def heart(request, event_id):
    event = ScheduleItem.objects.filter(id=event_id).first()
    event.hearts += 1
    event.save()
    return redirect("/")

def schedule2(request):
    return render(request, "schedule2.html")


def comment(request):
    pass


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, "login.html", {"message": "Logged out."})
    else:
        return render(request, "login.html", {"message": "You are already logged out."})
