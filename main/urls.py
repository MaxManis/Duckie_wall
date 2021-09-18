from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('login', user_login, name='login'),
    path('register', user_register, name='register'),
    path('logout', user_logout, name='logout'),
    path('profile_edit', profile_edit, name='profile_edit'),
    path('my_profile', my_profile, name='my_profile'),
    path('create', create, name='create'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)