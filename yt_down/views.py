# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404, HttpResponse
from .forms import Userform
from django.contrib.auth import authenticate, login, logout
from pytube import YouTube
from downloader.path import download_path
from .models import Video
import datetime
# Create your views here.


def signup(request):
    form = Userform()
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['curr_user'] = username
                return redirect('home')
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['curr_user'] = username
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid ID, please register first'})
    return render(request, 'login.html')


def logout_user(request):
    if request.session['curr_user']:
        del request.session['curr_user']
    logout(request)
    return redirect('home')


def get_download(request):
    if request.method == 'GET':
        url = request.GET['url']
        try:
            yt = YouTube(str(url))
            title = yt.title
            thumbnail = yt.thumbnail_url
            stream = yt.streams.filter(res="360p").last()
            path = download_path()
            stream.download(path)
            message = "Download in progress!"
            video = Video()
            curr_user = User.objects.get(username=request.session['curr_user'])
            video.user = curr_user
            video.video_link = str(url)
            video.video_name = title
            video.date = datetime.datetime.date()
            video.img_src = thumbnail
            video.save()
        except:
            message = "Enter a valid url"
        return render(request, "download.html", {'message': message})
