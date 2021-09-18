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


def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.get_user()
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Error of login!')
    else:
        form = ProfileEditForm()
    return render(request, 'main/profile_edit.html', {
        'form': form,
        'title': 'Login',
    })
