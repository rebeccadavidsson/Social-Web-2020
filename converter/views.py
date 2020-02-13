from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib.auth.decorators import permission_required


def index(request):
    context = {}
    return render(request, 'login.html', context)


def login_view(request):
    context = {}
    return render(request, 'login.html', context)


def register_view(request):
    context = {}
    return render(request, 'register.html', context)


def home_view(request):
    context = {}
    # van https://html.crumina.net/html-olympus/17-FriendGroups.html
    # ALS VOORBEELD
    return render(request, 'test.html', context)
