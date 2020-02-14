from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required


def index(request):
    context = {}
    # TODO

    print("OPENING HOMEPAGE")

    return render(request, 'home.html', context)


def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If user already exists, redirect to index
        if user is not None:
            login(request, user)
            return redirect("index")

        # TODO: Dit afmaken met registeren, model voor User aanmaken
        return redirect("index")

    return render(request, "login.html", {"message": "Incorrect name and/or password"})


def register_view(request):
    context = {}
    # TODO
    return render(request, 'register.html', context)


def home_view(request):
    context = {}
    # TODO
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {"message": "Logged out."})
