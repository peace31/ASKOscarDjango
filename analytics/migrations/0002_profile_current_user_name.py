# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-05 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Current_user_name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
