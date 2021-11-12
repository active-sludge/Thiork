from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from moderators.models import Vectis


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class VectisInline(admin.StackedInline):
    model = Vectis
    can_delete = False
    verbose_name_plural = 'vectis'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (VectisInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
