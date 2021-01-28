# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect, Http404, HttpResponse
from .forms import Userform
from django.contrib.auth import authenticate, login, logout
from pytube import YouTube
from django.contrib.auth.decorators import login_required
from downloader.path import download_path
from .models import Video
import datetime
from pytube.helpers import safe_filename
from pytube import Playlist
import os
import pathlib
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html", {'user': request.session['curr_user'], 'logged': True})
    return render(request, "home.html", {'user': ''})


def signup(request):
    form = Userform()
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user1 = authenticate(username=username, password=password)
            login(request, user1)
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
            return render(request, 'login.html', {'error': True})
    return render(request, 'login.html', {'error': ''})


@login_required(login_url='/downloader/login')
def logout_user(request):
    if request.session['curr_user']:
        del request.session['curr_user']
    logout(request)
    return redirect('home')


@login_required(login_url='/downloader/login')
def get_download(request):
    if request.method == 'GET':
        if(request.GET.get('url')):
            url = request.GET['url']
            try:
                if "playlist?list" in url : # checking whether url is playlist
                    playlist = Playlist(url)
                    
                    path = download_path()
                    video = Video()
                    curr_user = User.objects.get(
                        username=request.session['curr_user'])
                    video.user = curr_user
                    
                    for playlistvideo in playlist.videos:
                        
                        playlistvideo.streams.filter(res='360p').first().download(path)
                        # downloading entire playlist
                        
                    message = "Playlist Downloaded!"
                    for videourl in playlist.video_urls:
                        yt = YouTube(videourl)
                        title = yt.title 
                        video.embed_video = str(videourl)
                        video.video_link = str(videourl)
                        video.video_name = title
                        video.date = datetime.datetime.today()
                        video.save()
                else:
                    yt = YouTube(url) # if url is of a single video
                    title = yt.title
                    stream = yt.streams.filter(res='360p').first()
                    path = download_path()
                    stream.download(path)
                    message = "Download Complete!"
                    video = Video()
                    curr_user = User.objects.get(
                        username=request.session['curr_user'])
                    video.user = curr_user
                    video.embed_video = str(url)
                    video.video_link = str(url)
                    video.video_name = title
                    video.date = datetime.datetime.today()
                    video.save()
                
            except:
                message = "Enter a valid url"
                raise
            return render(request, "download.html", {'message': message, 'logged': True, 'user': request.session['curr_user']})
        else:
            return render(request, "download.html", {'message': '', 'logged': True, 'user': request.session['curr_user']})


@login_required(login_url='/downloader/login')
def profile(request):
    curr_user = User.objects.get(username=request.session['curr_user'])
    try:
        videos = Video.objects.filter(user=curr_user)
        context = {'videos': videos, 'logged': True,
                   'user': request.session['curr_user']}
    except Video.DoesNotExist:
        message = "You have no previous downloads"
        context = {'videos': [], 'message': message, 'logged': True,
                   'user': request.session['curr_user']}
    return render(request, "profile.html", context)


@login_required(login_url="/downloader/login")
def play_video(request, id):
    video = Video.objects.get(id=id)
    context = {'video': video.embed_video, 'title': video.video_name}
    return render(request, "player.html", context)
