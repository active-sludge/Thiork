from django.shortcuts import render


def index(request):
    return render(request, 'servitiums/servitiums.html')


def servitium(request):
    return render(request, 'servitiums/servitiums.html')


def search(request):
    return render(request, 'servitiums/servitiums.html')
