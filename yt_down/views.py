# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, Http404, HttpResponse
from .forms import Userform
from django.contrib.auth import authenticate, login, logout
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
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'form': form})
