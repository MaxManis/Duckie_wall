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

def home(request):
    user_id = request.user.id
    following = Follow.objects.filter(user_from=user_id).values('user_to')
    print(following)
    following_posts = Posts.objects.filter(user_id__in=following).select_related('user')
    return render(request, 'main/index.html', {
        "following": following,
        'following_posts': following_posts,
    })


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
    posts = Posts.objects.filter(user_id=user_id).select_related('user')
    followers = Follow.objects.filter(user_to=user_id).count()
    following = Follow.objects.filter(user_from=user_id).count()
    posts_cou = posts.count()
    return render(request, 'main/my_profile.html', {
        'user': user,
        'profile': profile,
        'posts': posts,
        'title': 'My profile',
        'followers': followers,
        'following': following,
        'posts_cou': posts_cou,
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
        # user_id = request.user.id
        # user = User.objects.get(pk=user_id)
        profile_form = ProfileEditForm()
        user_form = UserEditForm(initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
        })
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
            return redirect(reverse_lazy('one_post', args=[new_post.id]))
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

    views = Posts.objects.get(pk=post_id)
    views.views = F('views') + 1
    views.save()
    post = Posts.objects.get(pk=post_id)
    comments = Comments.objects.filter(post_id=post_id).select_related('post', 'user')

    return render(request, 'main/one_post.html', {
        'post': post,
        'title': post.content,
        'form': form,
        'comments': comments,
    })


def get_user(request, user_id):
    user_from = User.objects.get(pk=request.user.id)
    user_to = User.objects.get(pk=user_id)
    if_follow_2 = Follow.objects.filter(user_from=user_from, user_to=user_to).select_related('user_from', 'user_to')
    if request.method == 'POST':
        if if_follow_2:
            del_follow = Follow.objects.get(user_from=user_from, user_to=user_to)
            del_follow.delete()
            print('STOP FOLLOW: ' + str(del_follow))
        else:
            new_follow = Follow.objects.create(user_from=user_from, user_to=user_to)
            print(new_follow)
    profile = Profile.objects.get(user_id=user_id)
    posts = Posts.objects.filter(user_id=user_id).select_related('user')
    if_follow = Follow.objects.filter(user_from=user_from, user_to=user_to).select_related('user_from', 'user_to')
    return render(request, 'main/get_user.html', {
        'user': user_to,
        'profile': profile,
        'posts': posts,
        'title': 'profile',
        'if_follow': if_follow,
    })


def search(request):
    title_s = request.GET.get('qwery')
    if not title_s:
        return render(request, 'main/search.html', {
            'users': '',
            'title': 'Search',
        })
    user_s = User.objects.filter(username__icontains=title_s)
    print(user_s)
    return render(request, 'main/search.html', {
        'users': user_s,
        'title': 'Search',
    })