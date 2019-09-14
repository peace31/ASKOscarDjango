# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.db import models
from django.contrib.auth.models import User
from hashids import Hashids

# from Ask_Oskar.settings import REGISTRATION_URL
hashids = Hashids(min_length=4)


# Create your models here.

class shortlink(models.Model):
    short = models.URLField("Shorten URL", max_length=200, null=True, blank=True)
    url = models.URLField("URL", max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=False)
    expire_date = models.DateTimeField("Expire Time", null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="User Id", null=True, blank=True)

    # shorturl = "%s://%s/i/%s"%(request.scheme,request.META['HTTP_HOST'],short)
    def getShortURL(self):
        return self.url

    # Encodes Url to a short url
    @staticmethod
    def shorten(link):
        l, _ = shortlink.objects.get_or_create(url=link.url)
        # using library to encrypt id
        return str('%s' % hashids.encrypt(l.pk))

    @staticmethod
    def getURL(code):
        x = shortlink.objects.filter(short=code).first()
        return x.url if x else 'invalidurl/'  # IF CODE NOT FOUND THAN REDIRECT TO INVALID-CODE PAGE.

    def __unicode__(self):
        return self.url
