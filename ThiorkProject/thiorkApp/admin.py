from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from thiorkApp.models import Servitium, Inquiry, Eventum, Attendance, Vectis

admin.site.register(User, UserAdmin)
admin.site.register(Servitium)
admin.site.register(Inquiry)
admin.site.register(Eventum)
admin.site.register(Attendance)
admin.site.register(Vectis)
