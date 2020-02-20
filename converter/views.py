from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import permission_required


def index(request):
    context = {}
    # TODO
    return render(request, 'mainpage.html', context)


def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        print(username)
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If user already exists, redirect to index
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"message": "Invalid credentials."})

        # TODO: Dit afmaken met registeren, model voor User aanmaken
        # return redirect("index")
    return render(request, "login.html", {"message": None})


def register_view(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if not username or not password or not email or not first_name or not last_name:
            return render(request, "register.html", {"message": "Please fill in all fields."})
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"message": "This username is already taken."})
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = authenticate(request, username=username, password=password)
            print("succesfully registered")
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "register.html")

def personal_view(request):
    context = {}
    # TODO
    return render(request, 'personal.html', context)

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
