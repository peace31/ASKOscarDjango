from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import Profile
from pinax.referrals.models import Referral
import re


@receiver(post_save, sender=User)
def create_user_referral(sender, instance, created, **kwargs):
    if created:
        Referral.objects.create(user=instance)
