from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from psycopg2 import IntegrityError


def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def sign_up_user(request):
    if request.method == "GET":
        return render(request, 'pages/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'pages/signup.html',
                              {'form': UserCreationForm(),
                               'error': 'That user name has already has been taken. Please choose a new username.'})
        else:
            return render(request, 'pages/signup.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


@login_required
def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def log_in_user(request):
    if request.method == "GET":
        return render(request, 'pages/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pages/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('index')


def servitiums(request):
    return render(request, 'servitiums/servitiums.html')


def create_servitium(request):
    return render(request, 'pages/index.html')