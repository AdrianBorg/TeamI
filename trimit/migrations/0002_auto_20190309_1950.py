# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-09 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='profile_picture',
            field=models.ImageField(blank=True, default='C:\\Users\\borga\\Workspace\\TeamI\\staticDefaultPagePic.jpg', upload_to='user_profile_images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='C:\\Users\\borga\\Workspace\\TeamI\\staticDefaultUserPic.jpg', upload_to='user_profile_images'),
        ),
    ]
