# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_link = models.CharField(max_length=255)
    img_src = models.CharField(
        max_length=255, default='https://www.siechem.com/wp-content/uploads/2016/09/default-video.jpg')
    video_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.user.username
