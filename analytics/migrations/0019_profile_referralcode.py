# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0018_auto_20170916_0546'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='referralcode',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]