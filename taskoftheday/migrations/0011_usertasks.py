# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 12:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskoftheday', '0010_auto_20170819_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='userTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step1', models.BooleanField(default=False)),
                ('step2', models.BooleanField(default=False)),
                ('step3', models.BooleanField(default=False)),
                ('step1task1', models.BooleanField(default=False)),
                ('step1task2', models.BooleanField(default=False)),
                ('step1task3', models.BooleanField(default=False)),
                ('step1task4', models.BooleanField(default=False)),
                ('step2task1', models.BooleanField(default=False)),
                ('step2task2', models.BooleanField(default=False)),
                ('step2task3', models.BooleanField(default=False)),
                ('step2task4', models.BooleanField(default=False)),
                ('step3task1', models.BooleanField(default=False)),
                ('step3task2', models.BooleanField(default=False)),
                ('step3task3', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
