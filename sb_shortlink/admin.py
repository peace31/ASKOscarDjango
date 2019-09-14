# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import shortlink


# Register your models here.
class shortlinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'short', 'url', 'active')


admin.site.register(shortlink, shortlinkAdmin)
