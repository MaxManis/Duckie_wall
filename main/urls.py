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
    path('one_post/<int:post_id>/', one_post, name='one_post'),
    path('get_user/<int:user_id>/', get_user, name='get_user'),
    path('search/', search, name='search'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)