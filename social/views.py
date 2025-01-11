from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from .forms import *
from .models import Post
from taggit.models import Tag


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
    sent = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n {cd['email']}\n {cd['phone']}\n {cd['message']}"
            send_mail(cd['subject'], message, 'social.NetVibe.com',
                      ['fatemefarajian1374@gmail.com'], fail_silently=False)
            sent = True

    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form, 'sent': sent})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    context = {
        'posts': posts,
        'tag': tag,

    }

    return render(request, 'social/list.html', context)







def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'social/detail.html', {'post': post})