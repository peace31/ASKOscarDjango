# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('taskoftheday', '0015_usertask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='sequence_number',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
