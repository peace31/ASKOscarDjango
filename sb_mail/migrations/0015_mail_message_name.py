# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sb_mail', '0014_auto_20170929_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail_message',
            name='name',
            field=models.CharField(default='llllllllll', max_length=30, verbose_name='Name'),
            preserve_default=False,
        ),
    ]