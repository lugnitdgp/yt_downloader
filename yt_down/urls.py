from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import signup, login_user, get_download, home, logout_user, profile

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login_user, name='login'),
    path('download', get_download, name='download'),
    path('logout', logout_user, name='logout'),
    path('profile', profile, name="profile"),
]
