# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        # ('auth', '0008_alter_user_username_max_length'),
        ('sb_mail', '0026_auto_20171003_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='sb_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signup_group', models.ManyToManyField(to='auth.Group', verbose_name='Groups')),
            ],
            options={
                'verbose_name': 'Group Settings',
            },
        ),
    ]
