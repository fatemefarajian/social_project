from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'description', 'created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'created', 'active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'created', 'title']
