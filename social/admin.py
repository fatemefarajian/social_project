from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']


