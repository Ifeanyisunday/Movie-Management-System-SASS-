from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomerAdmin(UserAdmin):
    list_display = ('username', 'role')


admin.site.register(CustomUser, CustomerAdmin)
