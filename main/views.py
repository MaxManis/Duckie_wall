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
    return render(request, 'main/home.html')


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
    return render(request, 'main/my_profile.html', {
        'user': user,
        'profile': profile,
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
