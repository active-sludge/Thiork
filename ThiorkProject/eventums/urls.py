from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eventums'),
    path('<int:eventum_id>', views.eventum, name='eventum'),
    path('search', views.search, name='search'),
]