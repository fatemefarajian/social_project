from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *


def log_out(request):
    logout(request)
    return HttpResponse('شما خارج شدید')


def profile(request):
    return HttpResponse('شما وارد شدید')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'registration/edit_user.html', {'user_form': user_form})


def ticket(request):
    pass

