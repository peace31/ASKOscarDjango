# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import argparse
import webbrowser
import httplib2

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import flow_from_clientsecrets

from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, OAuth2WebServerFlow, GoogleCredentials
from pinax.referrals.models import Referral
from oauth2client import client, file, tools
from django.contrib.auth.models import User
from googleapiclient import sample_tools
import os
from taskoftheday.models import Guide, Step, Task, UserTaskHistory
from analytics.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from sb_mail.models import sbmail_template, sb_settings, mail_message
import traceback, sys, jsonpickle, json


# Create your views here.
@login_required(login_url='/login/')
@csrf_exempt
def settings(request):
    account = request.POST.get('account', '')
    if account == '' and request.GET.get('code', False) == False:
        profile = Profile.objects.filter(user_id=request.user.id).first()
        # GET REFERRAL OBJECT OF THIS USER 
        url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                                profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
        profilerank = profile.profilerank if profile else None
        return render(request, 'settings/settings.html', {'profile': profile, 'profilerank': profilerank, 'url': url})

    elif account == '':
        if request.GET.get('code', False):
            flow = client.flow_from_clientsecrets('client_secret_sb_webapp_GA.json',
                                                  scope='https://www.googleapis.com/auth/analytics',
                                                  redirect_uri="%s://%s%s" % (
                                                  request.scheme, request.META['HTTP_HOST'], '/settings/'),
                                                  prompt='select_account')

            google_authcode = request.GET['code']
            credentials = flow.step2_exchange(google_authcode)
            access_token1 = credentials.access_token
            refresh_token1 = credentials.refresh_token
            client_id = credentials.client_id
            client_secret = credentials.client_secret
            token_expiry = credentials.token_expiry
            token_uri = credentials.token_uri
            user_agent = credentials.user_agent
            revoke_uri = credentials.revoke_uri

            Profile.objects.filter(user_id=request.user.id).update(
                google_authcode=google_authcode,
                access_token=access_token1,
                refresh_token=refresh_token1,
                client_id=client_id,
                client_secret=client_secret,
                token_expiry=token_expiry,
                token_uri=token_uri,
                user_agent=user_agent,
                revoke_uri=revoke_uri
            )

            http_auth = credentials.authorize(httplib2.Http())

            service = build('analytics', 'v3', http_auth, cache_discovery=False)
            accounts = service.management().accounts().list().execute()

            if accounts.get('items'):
                account1 = []
                account2 = []
                for account in accounts.get('items'):
                    account1 = account1 + [account.get('name')]
                    account2 = account2 + [account.get('id')]
                zipped_data = zip(account1, account2)
                return render(request, 'settings/settings.html', {'accounts': zipped_data})
            else:
                profile = Profile.objects.filter(user_id=request.user.id).first()
                # GET REFERRAL OBJECT OF THIS USER 
                url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                                        profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
                profilerank = profile.profilerank if profile else None
                message = "You don't have analytics account "
                return render(request, 'settings/settings.html',
                              {'profile': profile, 'profilerank': profilerank, 'url': url, 'message': message})


    elif account:
        profile = Profile.objects.filter(user_id=request.user.id).first()

        access_token = profile.access_token
        refresh_token = profile.refresh_token
        client_id = profile.client_id
        client_secret = profile.client_secret
        token_expiry = profile.token_expiry
        token_uri = profile.token_uri
        user_agent = profile.user_agent
        revoke_uri = profile.revoke_uri

        credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, token_expiry, token_uri,
                                        'my-user-agent/1.0', revoke_uri)
        http_auth = credentials.authorize(httplib2.Http())
        service = build('analytics', 'v3', http_auth, cache_discovery=False)
        # Get a list of all the properties for the first account.

        profile1 = None
        properties = service.management().webproperties().list(accountId=account).execute()
        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')
            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(accountId=account, webPropertyId=property).execute()
            if profiles.get('items'):
                # return the first view (profile) id.
                profile1 = profiles.get('items')[0].get('id')

        if profile1 == None:
            profile = Profile.objects.filter(user_id=request.user.id).first()
            # GET REFERRAL OBJECT OF THIS USER 
            url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                                    profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
            profilerank = profile.profilerank if profile else None
            message = "Your account  don't have sufficient permission "
            return render(request, 'settings/settings.html',
                          {'profile': profile, 'profilerank': profilerank, 'url': url, 'message': message})

        service = build('analytics', 'v4', http_auth, cache_discovery=False)
        message = 'Not have permission of'
        try:
            conversion_rate = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:goalConversionRateAll'}]
                        }]
                }
            ).execute()

            for ccr in conversion_rate['reports']:
                for rate in ccr['data']['totals']:
                    conversion_vals = rate['values']
                    # Profile._meta.get_field('current_conversion_rate').default = float(vals[0])
                    # Profile._meta.get_field('optimal_conversion_rate').default = float(vals[0])
        except:
            # raise Exception('Permission Denied')
            conversion_vals = [0]
            message = message + ' Conversion Rate '
            pass
            # return sb_traceback(request)
        try:
            bounce_rate = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:bounceRate'}],
                        }]
                }
            ).execute()

            for cbr in bounce_rate['reports']:
                for rate in cbr['data']['totals']:
                    bounce_vals = rate['values']
                    # Profile._meta.get_field('current_bounce_rate').default = float(vals[0])
                    # Profile._meta.get_field('optimal_bounce_rate').default = float(vals[0])
        except:
            # print traceback.print_exc()
            # print e
            bounce_vals = [0]
            message = message + ' Bounce Rate '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            metric_expression = {
                'expression': 'ga:transactionRevenue/ga:transactions',
                'formattingType': 'FLOAT'
            }

            avg_order_value = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [metric_expression],
                        }]
                }
            ).execute()

            for caov in avg_order_value['reports']:
                for order in caov['data']['totals']:
                    order_value = order['values']
                    # Profile._meta.get_field('current_average_order_value').default = float(value[0])
                    # Profile._meta.get_field('optimal_average_order_value').default = float(value[0])
        except:
            order_value = [0]
            message = message + ' Average Order Value '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            cart_abandonment_rate = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:goalAbandonRateAll'}],
                        }]
                }
            ).execute()

            for ccar in cart_abandonment_rate['reports']:
                for cart_rate in ccar['data']['totals']:
                    cart_vals = cart_rate['values']
                    # Profile._meta.get_field('current_shopping_cart_abandonment_rate').default = float(cart_vals[0])
                    # Profile._meta.get_field('optimal_shopping_cart_abandonment_rate').default = float(cart_vals[0])
        except:
            cart_vals = [0]
            message = message + ' Cart Abandonment Rate '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            revenue_per_user = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:revenuePerUser'}],
                            # "dimensions":[{"name":"ga:transactionId"}],
                        }]
                }
            ).execute()

            for crpu in revenue_per_user['reports']:
                for revenue in crpu['data']['totals']:
                    revenue_vals = revenue['values']
                    # Profile._meta.get_field('current_revenue_per_user').default = float(vals[0])
                    # Profile._meta.get_field('optimal_revenue_per_user').default = float(vals[0])
        except:
            revenue_vals = [0]
            message = message + ' Revenue Per User '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            traffic = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:organicSearches'}],
                            "dimensions": [{"name": "ga:month"}],
                        }]
                }
            ).execute()

            for current_montn_traffic in traffic['reports']:
                for dimension in current_montn_traffic['data']['rows']:
                    pass

                a = max(int(d) for d in dimension['dimensions'])
                for traffic in current_montn_traffic['data']['totals']:
                    traffic_vals = cart_rate['values']
                    # Profile._meta.get_field('optimal_traffic').default = float(traffic_vals[0])

            # Analytics matrics of Traffic This Month
            traffic_this_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:organicSearches'}],
                            "dimensions": [{"name": "ga:month"}],
                            "dimensionFilterClauses": [
                                {
                                    "filters": [
                                        {
                                            "dimensionName": "ga:month",
                                            "operator": "EXACT",
                                            "expressions": ["0%s" % a]
                                        }
                                    ]
                                }]
                        }
                    ]
                }
            ).execute()

            for cttm in traffic_this_month['reports']:
                for traffic in cttm['data']['totals']:
                    traffic_this_vals = traffic['values']
                    # Profile._meta.get_field('traffic_this_month').default = float(vals[0])
        except:
            traffic_this_vals = [0]
            message = message + ' Traffic This Month '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            # Analytics matrics of Traffic Last Month
            traffic_last_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:organicSearches'}],
                            # "dimensions":[{"name":"ga:month"}],
                        }
                    ]
                }
            ).execute()

            for ctlm in traffic_last_month['reports']:
                for traffic_last in ctlm['data']['totals']:
                    traffic_last_vals = traffic_last['values']
                    # Profile._meta.get_field('traffic_last_month').default = float(last_vals[0])
        except:
            traffic_last_vals = [0]
            message = message + ' Traffic Last Month '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            # Analytics matrics of Revenue This Month
            revenue_this_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            "dimensions": [{"name": "ga:month"}],
                        }]
                }
            ).execute()

            for crtm in revenue_this_month['reports']:
                for revenue in crtm['data']['totals']:
                    revenue_this_vals = revenue['values']
                    # Profile._meta.get_field('revenue_this_month').default = float(vals[0])
        except:
            revenue_this_vals = [0]
            message = message + ' Revenue This Month '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            # Analytics matrics of Revenue Last Month
            revenue_last_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '60daysAgo', 'endDate': '30daysago'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            # "dimensions":[{"name":"ga:month"}],
                        }]
                }
            ).execute()

            for crlm in revenue_last_month['reports']:
                for revenue in crlm['data']['totals']:
                    revenue_last_vals = revenue['values']
                    # Profile._meta.get_field('revenue_last_month').default = float(vals[0])
        except:
            revenue_last_vals = [0]
            message = message + ' Revenue Last Month '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        try:
            optimal_revenue = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile1,
                            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            # "dimensions":[{"name":"ga:month"}],
                        }]
                }
            ).execute()

            for optrev in optimal_revenue['reports']:
                for revenue in optrev['data']['totals']:
                    optimal_revenue_vals = revenue['values']
                    # Profile._meta.get_field('optimal_revenue').default = float(vals[0])
        except:
            optimal_revenue_vals = [0]
            message = message + ' Optimal Revenue '
            pass
            # return sb_traceback(request)
            # raise Exception('Permission Denied')

        profile = Profile.objects.filter(user_id=request.user.id).first()
        # if not UserTaskHistory:
        #   guide = Guide.objects.get(pk=8)
        #   steps = Step.objects.filter(guide=guide.id).first()
        #   tasks = Task.objects.filter(step=steps).first()
        # else:
        #   pass
        user = User.objects.get(id=request.user.id)
        if not profile:
            pr = Profile.objects.create(current_conversion_rate=float(conversion_vals[0]),
                                        optimal_conversion_rate=float(conversion_vals[0]),
                                        current_bounce_rate=float(bounce_vals[0]),
                                        optimal_bounce_rate=float(bounce_vals[0]),
                                        current_average_order_value=float(order_value[0]),
                                        optimal_average_order_value=float(order_value[0]),
                                        current_shopping_cart_abandonment_rate=float(cart_vals[0]),
                                        optimal_shopping_cart_abandonment_rate=float(cart_vals[0]),
                                        traffic_last_month=float(traffic_last_vals[0]),
                                        traffic_this_month=float(traffic_this_vals[0]),
                                        optimal_traffic=float(revenue_this_vals[0]),
                                        revenue_last_month=float(revenue_last_vals[0]),
                                        revenue_this_month=float(conversion_vals[0]),
                                        optimal_revenue=float(optimal_revenue_vals[0]),
                                        current_revenue_per_user=float(revenue_vals[0]),
                                        optimal_revenue_per_user=float(revenue_vals[0]),
                                        current_user_name=request.user.username,
                                        user_id=user,
                                        connected=True,
                                        accountid=account,
                                        )
            pr.save()
        else:
            Profile.objects.filter(user_id=request.user.id).update(
                current_conversion_rate=float(conversion_vals[0]),
                optimal_conversion_rate=float(conversion_vals[0]),
                current_bounce_rate=float(bounce_vals[0]),
                optimal_bounce_rate=float(bounce_vals[0]),
                current_average_order_value=float(order_value[0]),
                optimal_average_order_value=float(order_value[0]),
                current_shopping_cart_abandonment_rate=float(cart_vals[0]),
                optimal_shopping_cart_abandonment_rate=float(cart_vals[0]),
                traffic_last_month=float(traffic_last_vals[0]),
                traffic_this_month=float(traffic_this_vals[0]),
                optimal_traffic=float(revenue_this_vals[0]),
                revenue_last_month=float(revenue_last_vals[0]),
                revenue_this_month=float(conversion_vals[0]),
                optimal_revenue=float(optimal_revenue_vals[0]),
                current_revenue_per_user=float(revenue_vals[0]),
                optimal_revenue_per_user=float(revenue_vals[0]),
                current_user_name=request.user.username,
                connected=True,
                accountid=account,
            )

        profile = Profile.objects.filter(user_id=request.user.id).first()

        # GET REFERRAL OBJECT OF THIS USER 
        url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                                profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''

        profilerank = profile.profilerank if profile else None

        message = '' if message == 'Not have permission of' else message

        return render(request, 'settings/settings.html',
                      {'profile': profile, 'profilerank': profilerank, 'url': url, 'message': message})


@login_required(login_url='/login/')
def GoogleAuth(request):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     parents=[tools.argparser], add_help=False)
    flags = parser.parse_args([])
    flow = client.flow_from_clientsecrets('client_secret_sb_webapp_GA.json',
                                          scope='https://www.googleapis.com/auth/analytics.readonly',
                                          redirect_uri="%s://%s%s" % (
                                          request.scheme, request.META['HTTP_HOST'], '/settings/',),
                                          prompt='consent')
    auth_url = flow.step1_get_authorize_url()
    return redirect(auth_url)


@login_required(login_url='/login/')
def GoogleAuthDisconnect(request):
    Profile.objects.filter(user_id=request.user.id).update(connected=False, accountid=None)
    profile = Profile.objects.filter(user_id=request.user.id).first()
    url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                            profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
    profilerank = profile.profilerank if profile else None
    if not profile:
        profile = {}
    return render(request, 'settings/settings.html', {'profile': profile, 'profilerank': profilerank, 'url': url})


@login_required(login_url='/login/')
@csrf_exempt
def massreferral(request):
    print ('@@@', request.POST.get('account'))
    profile = Profile.objects.filter(user_id=request.user.id).first()
    # GET REFERRAL OBJECT OF THIS USER
    url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                            profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
    profilerank = profile.profilerank if profile else None
    recipients = request.POST['recipients']
    message1 = '''
        Welcome to Askoskara,<br>
        kindly visit through link given below for the signup.<br><br>

        <a href="%s" target="_blank">Click For signup</a><br><br>  

        Team<br>
        Askoskara
    ''' % url

    msg1 = ('subject 1', message1, 'polo@polo.com', [recipients])
    msg2 = ('subject 2', 'message 2', 'polo@polo.com', [recipients])
    res = send_mass_mail((msg1, msg2), fail_silently=False)
    return render(request, 'settings/settings.html',
                  {'profile': profile, 'url': url, 'message': 'your referral email receipt list sent successfully',
                   'profilerank': profilerank})


def profile(request):
    return render(request, 'settings/profile.html')


def payments(request):
    return render(request, 'settings/payments.html')


def sb_traceback(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()
    # GET REFERRAL OBJECT OF THIS USER 
    url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'],
                            profile.profilelink.short) if profile and profile.profilelink and profile.profilelink.short else ''
    profilerank = profile.profilerank if profile else None
    message = "Your account  don't have sufficient permission "
    return render(request, 'settings/settings.html',
                  {'profile': profile, 'profilerank': profilerank, 'url': url, 'message': message})
