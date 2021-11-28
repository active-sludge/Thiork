from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from psycopg2 import IntegrityError
from .forms import ServitiumForm
from .models import Servitium, Vectis


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
                vectis = Vectis.objects.create(user=user)
                vectis.save()
                login(request, vectis.user)
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
        vectis = Vectis.objects.first(user=user)
        if user is None:
            return render(request, 'pages/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('index')


def servitiums(request):
    all_servitiums = Servitium.objects.all()
    return render(request, 'servitiums/servitiums.html', {'all_servitiums': all_servitiums})


def create_servitium(request):
    servitium_form = ServitiumForm()
    if request.method == 'GET':
        return render(request, 'servitiums/create_servitium.html', {'form': servitium_form})
    else:
        try:
            form = ServitiumForm(request.POST)
            new_servitium = form.save(commit=False)
            new_servitium.status = 'Available'
            new_servitium.owner = request.user
            new_servitium.save()
            return redirect('servitiums')
        except ValueError:
            return render(request, 'servitiums/create_servitium.html',
                          {'form': ServitiumForm(), 'error': 'Bad data entry. Try again.'})
