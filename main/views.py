from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.db.models import Max, Count, Q, Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail

from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'main/index.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You was successfully registered!")
            return redirect('home')
        else:
            messages.error(request, 'Error of register!')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {
            'form': form,
            'title': 'Registration',
        })


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(form.changed_data)
        if form.is_valid():
            user = form.get_user()
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Error of login!')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {
        'form': form,
        'title': 'Login',
    })


def user_logout(request):
    logout(request)
    return redirect('login')


def my_profile(request):
    user_id = request.user.id
    user = request.user
    print(user)
    profile = Profile.objects.get(user_id=user_id)
    posts = Posts.objects.filter(user_id=user_id)
    return render(request, 'main/my_profile.html', {
        'user': user,
        'profile': profile,
        'posts': posts,
        'title': 'My profile',
    })


def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('home')
        else:
            messages.error(request, 'Error of login!')
    else:
        profile_form = ProfileEditForm()
        user_form = UserEditForm()
    return render(request, 'main/profile_edit.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'title': 'Login',
    })


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            content = form.cleaned_data['content']
            photo = form.cleaned_data['photo']
            new_post = Posts.objects.create(user=user, content=content, photo=photo)
            # form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'main/create.html', {
        'form': form,
        'title': 'Create',
    })


def one_post(request, post_id):
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            post = Posts.objects.get(pk=post_id)
            content = form.cleaned_data['content']
            new_comment = Comments.objects.create(user=user, post=post, content=content)
            return redirect(reverse_lazy('one_post', args=[post_id]))
    else:
        form = CommentsForm()
    views_plus = Posts.objects.get(pk=post_id)
    views_plus.views = F('views') + 1
    views_plus.save()
    comments = Comments.objects.filter(post_id=post_id)
    post = Posts.objects.get(pk=post_id)

    return render(request, 'main/one_post.html', {
        'post': post,
        'title': post.content,
        'form': form,
        'comments': comments,
    })


def get_user(request, user_id):
    user_from = User.objects.get(pk=request.user.id)
    user_to = User.objects.get(pk=user_id)
    if_follow_2 = Follow.objects.filter(user_from=user_from, user_to=user_to)
    if request.method == 'POST':
        if if_follow_2:
            del_follow = Follow.objects.get(user_from=user_from, user_to=user_to)
            del_follow.delete()
            print('STOP FOLLOW: ' + str(del_follow))
        else:
            new_follow = Follow.objects.create(user_from=user_from, user_to=user_to)
            print(new_follow)
    # user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    posts = Posts.objects.filter(user_id=user_id)
    if_follow = Follow.objects.filter(user_from=user_from, user_to=user_to)
    return render(request, 'main/get_user.html', {
        'user': user_to,
        'profile': profile,
        'posts': posts,
        'title': 'My profile',
        'if_follow': if_follow,
    })


def search(request):
    title_s = request.GET.get('q')
    # if title_s == None:
    #     title_s = 'nope'
    # if '/' in title_s:
    #     title_s = title_s[:title_s.find('/')]
    user_s = User.objects.filter(username__icontains=title_s)
    print(user_s)
    # profile = Profile.objects.filter(user_id=user_s)
    #print(profile)
        # .select_related('category')
    return render(request, 'main/search.html', {
        'users': user_s,
        'title': 'Search',
    })