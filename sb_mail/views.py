# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import sbmail_template


def mails(request):
    # print sbmail_template.objects.filter(id=1).get()

    return render(request, 'landing_index.html')
# Create your views here.
