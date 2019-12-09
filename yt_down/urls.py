from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import signup, login_user, get_download

urlpatterns = [
    path('signup', signup), 
    path('login', login_user),
    path('download', get_download),
]
