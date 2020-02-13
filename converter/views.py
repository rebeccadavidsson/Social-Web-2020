from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib.auth.decorators import permission_required


def index(request):
    context = {}
    return render(request, 'home.html', context) #TODO


def login_view(request):
    context = {}
    return render(request, 'login.html', context)


@permission_required('admin.can_view_csv')
def load_csv(request):

    file = request.FILES['file']

    if not file.name.endswith('.csv'):
        return "TODO"

    return "TOODOOOO"
