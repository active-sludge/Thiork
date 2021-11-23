from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('servitiums', views.servitiums, name='servitiums'),
    path('eventums', views.eventums, name='eventums'),

    # Auth
    path('signup', views.sign_up_user, name='signupuser'),
    path('logout', views.log_out_user, name='logoutuser'),
    path('login/', views.log_in_user, name='loginuser'),

]