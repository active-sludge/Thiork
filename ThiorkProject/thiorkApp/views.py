from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from psycopg2 import IntegrityError
from .forms import ServitiumForm, VectisForm, EventumForm
from .models import Servitium, Vectis, Inquiry, Status, Eventum
from django.template import Context


def index(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def sign_up_user(request):
    if request.method == "GET":
        return render(request, 'pages/signup.html', {'form': VectisForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                form = VectisForm(data=request.POST, files=request.FILES)
                if form.is_valid():
                    vectis = form.save(commit=False)
                    vectis.save()
                    login(request, vectis)
                    return redirect('index')

                return render(request, 'pages/signup.html',
                              {'form': form,
                               'error': form.errors})

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
    all_servitiums = Servitium.objects.all()
    return render(request, 'servitiums/servitiums.html', {'all_servitiums': all_servitiums})


def create_servitium(request):
    servitium_form = ServitiumForm()
    if request.method == 'GET':
        return render(request, 'servitiums/create_servitium.html', {'form': servitium_form})
    else:
        try:
            form = ServitiumForm(request.POST, request.FILES)
            if form.is_valid():
                new_servitium = form.save(commit=False)
                new_servitium.status = 'Available'
                new_servitium.owner = request.user
                new_servitium.save()
                return redirect('servitiums')
        except ValueError:
            return render(request, 'servitiums/create_servitium.html',
                          {'form': ServitiumForm(), 'error': 'Bad data entry. Try again.'})


def servitium_detail(request, servitium_pk):
    servitium = get_object_or_404(Servitium, id=servitium_pk)
    if request.method == 'GET':
        form = ServitiumForm(instance=servitium)
        try:
            inquiry = Inquiry.objects.get(servitium=servitium)
        except Inquiry.DoesNotExist:
            inquiry = None

        return render(request, 'servitiums/servitium.html', {'servitium': servitium, 'inquiry': inquiry, 'form': form})
    else:
        try:
            form = ServitiumForm(request.POST, instance=servitium)
            form.save()
            return redirect('servitiums')
        except ValueError:
            pass


def request_servitium(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        Inquiry.objects.get_or_create(servitium=servitium, receiver=request.user, status=Status.PENDING.value)

        servitium.status = Status.PENDING.value
        servitium.save()

        message = 'You requested the Servitium. We will shared the contact info of the owner, if they accept your ' \
                  'request. We will let you know. '
    return render(request, 'servitiums/servitium.html', {'servitium': servitium, 'message': message})


def accept_request(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        inquiry = Inquiry.objects.get(servitium=servitium)
        print(inquiry.receiver)
        receiver = inquiry.receiver
        receiver.credit -= servitium.credit
        receiver.save()

        owner = inquiry.servitium.owner
        owner.credit += servitium.credit
        owner.save()

        inquiry.status = Status.HANDSHAKEN.value
        inquiry.save()

        servitium.status = Status.HANDSHAKEN.value
        servitium.save()

        message = 'You accepted the servitium request. Your contact info will be shared with the requester.'

    return render(request, 'servitiums/servitium.html',
                  {'servitium': servitium, 'inquiry': inquiry, 'message': message, 'status': 'Handshaken'})


def reject_request(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        inquiry = Inquiry.objects.get(servitium=servitium)
        print(inquiry.receiver)
        inquiry.delete()

        servitium.status = Status.AVAILABLE.value
        servitium.save()

        message = 'You rejected the servitium request.'

    return render(request, 'servitiums/servitium.html',
                  {'servitium': servitium, 'message': message, 'status': 'Available'})


def profile_page(request):
    servitiums = Servitium.objects.filter(owner=request.user)

    context = {
        'profile': request.user,
        'servitiums': servitiums,
    }
    return render(request, 'pages/profilePage.html', context)


def complete_servitium(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        inquiry = Inquiry.objects.get(servitium=servitium)
        inquiry.status = Status.COMPLETED.value
        inquiry.save()

        servitium.status = Status.COMPLETED.value
        servitium.save()

        message = 'Congratulations! You completed the servitium.'

    return render(request, 'servitiums/servitium.html',
                  {'servitium': servitium, 'message': message, 'status': 'Completed'})


def cancel_servitium(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        inquiry = Inquiry.objects.get(servitium=servitium)
        inquiry.delete()

        servitium.status = Status.AVAILABLE.value
        servitium.save()

        message = 'You canceled the servitium.'

    return render(request, 'servitiums/servitium.html',
                  {'servitium': servitium, 'message': message, 'status': 'Available'})


def rate_servitium(request, servitium_pk):
    servitium = get_object_or_404(Servitium, pk=servitium_pk)
    if request.method == 'POST':
        inquiry = Inquiry.objects.get(servitium=servitium)
        print(inquiry.receiver)
        inquiry.delete()

        servitium.status = Status.AVAILABLE.value
        servitium.save()

        message = 'You rated this servitium! Thanks for the feedback.'

    return render(request, 'servitiums/servitium.html',
                  {'servitium': servitium, 'message': message, 'status': 'Available'})


def eventums(request):
    all_eventums = Eventum.objects.all()
    return render(request, 'eventums/eventums.html', {'all_eventums': all_eventums})


def create_eventum(request):
    eventum_form = EventumForm()
    if request.method == 'GET':
        return render(request, 'eventums/create_eventum.html', {'form': eventum_form})
    else:
        try:
            form = EventumForm(request.POST, request.FILES)
            print(request.POST)
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                new_eventum = form.save(commit=False)
                new_eventum.host = request.user
                new_eventum.save()
                return redirect('eventums')
        except ValueError:
            return render(request, 'eventums/create_eventum.html',
                          {'form': form, 'error': 'Bad data entry. Try again.'})


def eventum_detail(request):
    return None