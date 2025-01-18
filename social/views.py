from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .forms import *
from .models import *
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
    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
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
    comments = post.comments.filter(active=True)
    form = CommentForm
    context = {

        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'social/detail.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.name = request.user
        comment.save()
    context = {

        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comments.html', context)


def create_post(request):
    if request.method == 'POST':
        form = CreationPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CreationPostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreationPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CreationPostForm(instance=post)
    return render(request, 'forms/create_post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('social:delete_post_success')

    return render(request, 'forms/delete_post.html', {'post': post})


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (Post.objects.annotate(
                similarity=TrigramSimilarity('tags', query) +
                           TrigramSimilarity('description', query))
                       .filter(similarity__gt=0.1).order_by('similarity'))

    context = {
            'query': query,
            'results': results,
            }
    return render(request, 'social/search.html', context)
