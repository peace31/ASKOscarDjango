from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taskoftheday.models import Guide
from taskoftheday.models import Step
from taskoftheday.models import Task
from pinax.referrals.models import Referral, ReferralResponse
from sb_shortlink.models import shortlink


# Create your models here.

class Profile(models.Model):
    # Conversion rate
    current_conversion_rate = models.FloatField(default=0.0)
    optimal_conversion_rate = models.FloatField(default=0.0)

    # Bounce rate
    current_bounce_rate = models.FloatField(default=0.0)
    optimal_bounce_rate = models.FloatField(default=0.0)

    # Average order value
    current_average_order_value = models.FloatField(default=0.0)
    optimal_average_order_value = models.FloatField(default=0.0)

    # Shopping cart abandonment
    current_shopping_cart_abandonment_rate = models.FloatField(default=0.0)
    optimal_shopping_cart_abandonment_rate = models.FloatField(default=0.0)

    # Traffic
    traffic_last_month = models.FloatField(default=0.0)
    traffic_this_month = models.FloatField(default=0.0)
    optimal_traffic = models.FloatField(default=0.0)

    # Revenue
    revenue_last_month = models.FloatField(default=0.0)
    revenue_this_month = models.FloatField(default=0.0)
    optimal_revenue = models.FloatField(default=0.0)

    # Revenue per user
    current_revenue_per_user = models.FloatField(default=0.0)
    optimal_revenue_per_user = models.FloatField(default=0.0)

    current_user_name = models.CharField(max_length=40, default='', blank=True, null=True)
    user_id = models.ForeignKey(User, default=0, blank=True, null=True)
    connected = models.BooleanField(default=False)

    current_guide_id = models.ForeignKey(Guide, blank=True, null=True)
    current_step_id = models.ForeignKey(Step, blank=True, null=True)
    current_task_id = models.ForeignKey(Task, blank=True, null=True)
    google_authcode = models.CharField(max_length=100, default='', blank=True, null=True)
    access_token = models.CharField(max_length=200, default='', blank=True, null=True)
    refresh_token = models.CharField(max_length=200, default='', blank=True, null=True)
    client_id = models.CharField(max_length=200, default='', blank=True, null=True)
    client_secret = models.CharField(max_length=200, default='', blank=True, null=True)
    token_expiry = models.CharField(max_length=200, default='', blank=True, null=True)
    token_uri = models.CharField(max_length=200, default='', blank=True, null=True)
    user_agent = models.CharField(max_length=200, default='', blank=True, null=True)
    revoke_uri = models.CharField(max_length=200, default='', blank=True, null=True)

    # PROFILE RANK FIELD
    profilerank = models.IntegerField(default=0)
    referral = models.ForeignKey(Referral, blank=True, null=True)

    rank = models.IntegerField(null=True)
    profilelink = models.ForeignKey(shortlink, blank=True, null=True)
    accountid = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        ordering = ('-profilerank',)
