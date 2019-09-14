# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from sb_shortlink.models import shortlink


# Create your views here.

def verifyurl(request, short):
    # print '@@@',short
    # x = shortlink.objects.filter(short=short).first()
    # return redirect(x.getShortURL())
    return redirect(shortlink.getURL(short))
