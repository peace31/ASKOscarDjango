from sb_mail.models import mail_message
from analytics.models import Profile

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import argparse
import webbrowser
import httplib2

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, AccessTokenCredentials, OAuth2WebServerFlow, GoogleCredentials
from oauth2client import client, file, tools
from django.contrib.auth.models import User
import os
from Ask_Oskar.settings import LOGGING
from . import views


def mail_sending():
    messages = mail_message.objects.filter(status="Queue")
    for message in messages:
        message._send()


def analytics_job():
    for profile1 in Profile.objects.all():

        if profile1.connected == True:
            access_token = profile1.access_token
            refresh_token = profile1.refresh_token
            google_authcode = profile1.google_authcode
            client_id = profile1.client_id
            client_secret = profile1.client_secret
            token_expiry = profile1.token_expiry
            token_uri = profile1.token_uri
            revoke_uri = profile1.revoke_uri
            account = profile1.accountid
            # credentials = AccessTokenCredentials(access_token,'my-user-agent/1.0')
            credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, token_expiry,
                                            token_uri, 'my-user-agent/1.0', revoke_uri)
            http_auth = credentials.authorize(httplib2.Http())
            # http_auth = credentials.authorize(httplib2.Http())
            service = build('analytics', 'v3', http_auth, cache_discovery=False)

            # accounts = service.management().accounts().list().execute()
            # if accounts.get('items'):
            # 	account = accounts.get('items')[0].get('id')

            properties = service.management().webproperties().list(accountId=account).execute()
            if properties.get('items'):
                property = properties.get('items')[0].get('id')

                profiles = service.management().profiles().list(accountId=account, webPropertyId=property).execute()
                if profiles.get('items'):
                    profile = profiles.get('items')[0].get('id')

            service = build('analytics', 'v4', http_auth, cache_discovery=False)

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
                pass

            Profile.objects.filter(user_id=profile1.user_id).update(
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
                access_token=access_token
            )
