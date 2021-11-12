from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='servitiums'),
    path('<int:servitium_id>', views.servitium, name='servitiums'),
    path('search', views.search, name='search'),
]