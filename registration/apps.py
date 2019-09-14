from __future__ import unicode_literals

from django.apps import AppConfig
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from registration.signals import create_user_referral


# FOR REFERRAL CONFIGURE APP REGISTRATION. AND SET CREATE AND SAVE USER WITH @receiver decorator.
class RegistrationConfig(AppConfig):
    name = 'registration'
    verbose_name = _('registration')

    def ready(self):
        @receiver(create_user_referral, sender=User)
