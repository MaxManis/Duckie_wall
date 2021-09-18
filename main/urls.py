from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', user_login, name='login'),
    path('register', user_register, name='register'),
    path('logout', user_logout, name='logout'),
    path('profile_edit', profile_edit, name='profile_edit'),
]