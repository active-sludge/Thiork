from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from thiorkApp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup', views.sign_up_user, name='signupuser'),
    path('logout', views.log_out_user, name='logoutuser'),
    path('login', views.log_in_user, name='loginuser'),
    path('profile', views.profile_page, name='profilepage'),

    # Pages
    path('', views.index, name='index'),
    path('about', views.about, name='about'),

    # Servitium
    path('servitiums', views.servitiums, name='servitiums'),
    path('create_servitium', views.create_servitium, name='create_servitium'),
    path('servitium/<int:servitium_pk>', views.servitium_detail, name='servitium_detail'),
    path('servitium/<int:servitium_pk>/request', views.request_servitium, name='request_servitium'),
    path('servitium/<int:servitium_pk>/accept', views.accept_request, name='accept_request'),
    path('servitium/<int:servitium_pk>/reject', views.reject_request, name='reject_request'),
    path('servitium/<int:servitium_pk>/complete', views.complete_servitium, name='complete_servitium'),
    path('servitium/<int:servitium_pk>/cancel', views.cancel_servitium, name='cancel_servitium'),
    path('servitium/<int:servitium_pk>/rate', views.rate_servitium, name='rate_servitium'),

    # Eventum



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
