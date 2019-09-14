# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import argparse
import webbrowser

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import flow_from_clientsecrets
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from django.contrib.auth.models import User
from googleapiclient import sample_tools
import os
from taskoftheday.models import Guide
from taskoftheday.models import Step
from taskoftheday.models import Task, UserTaskHistory

from analytics.models import Profile


# Create your views here.
@login_required(login_url='/login/')
def settings(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()
    # print profile.connected
    # print profile.current_user_name,profile.id
    return render(request, 'settings/settings.html', {'profile': profile})


@login_required(login_url='/login/')
def GoogleAuth(request):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     parents=[tools.argparser], add_help=False)
    flags = parser.parse_args([])

    flow = client.flow_from_clientsecrets(
        '1071534795399-9q9urdlq845cu060e7isa56usjsdnu3o.apps.googleusercontent.com.json',
        scope='https://www.googleapis.com/auth/analytics.readonly',
        redirect_uri='askoskara.snippetbucket.com')

    storage = file.Storage('analytics_%s' % request.user.id + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    http_auth = credentials.authorize(httplib2.Http())

    service = build('analytics', 'v4', http_auth)

    # Profile._meta.get_field('current_user_name').default = request.user.username
    # Profile._meta.get_field('user_id').default = request.user.username
    try:
        conversion_rate = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:goalConversionRateAll'}]
                    }]
            }
        ).execute()
        # print ('Conversion Rate..................',conversion_rate)
        # print('')

        for ccr in conversion_rate['reports']:
            for rate in ccr['data']['totals']:
                conversion_vals = rate['values']
                # Profile._meta.get_field('current_conversion_rate').default = float(vals[0])
                # Profile._meta.get_field('optimal_conversion_rate').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        bounce_rate = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:bounceRate'}]
                    }]
            }
        ).execute()
        # print ('Bounce Rate..................',bounce_rate)
        # print('')

        for cbr in bounce_rate['reports']:
            for rate in cbr['data']['totals']:
                bounce_vals = rate['values']
                # Profile._meta.get_field('current_bounce_rate').default = float(vals[0])
                # Profile._meta.get_field('optimal_bounce_rate').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        metric_expression = {
            'expression': 'ga:transactionRevenue/ga:transactions',
            'formattingType': 'FLOAT'
        }
        # print ('Metrics Expression.................',metric_expression)
        # print('')

        avg_order_value = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [metric_expression],
                    }]
            }
        ).execute()
        # print ('Average Order Value...............',avg_order_value)
        # print('')

        for caov in avg_order_value['reports']:
            for order in caov['data']['totals']:
                order_value = order['values']
                # Profile._meta.get_field('current_average_order_value').default = float(value[0])
                # Profile._meta.get_field('optimal_average_order_value').default = float(value[0])
    except:
        raise Exception('Permission Denied')

    try:
        cart_abandonment_rate = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:goalAbandonRateAll'}],
                    }]
            }
        ).execute()
        # print ('cart_abandonment_rate ..................',cart_abandonment_rate)
        # print('')

        for ccar in cart_abandonment_rate['reports']:
            for cart_rate in ccar['data']['totals']:
                cart_vals = cart_rate['values']
                # Profile._meta.get_field('current_shopping_cart_abandonment_rate').default = float(cart_vals[0])
                # Profile._meta.get_field('optimal_shopping_cart_abandonment_rate').default = float(cart_vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        revenue_per_user = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:revenuePerUser'}],
                        # "dimensions":[{"name":"ga:transactionId"}],
                    }]
            }
        ).execute()
        # print ('Revenue Per User................',revenue_per_user)
        # print('')

        for crpu in revenue_per_user['reports']:
            for revenue in crpu['data']['totals']:
                revenue_vals = revenue['values']
                # Profile._meta.get_field('current_revenue_per_user').default = float(vals[0])
                # Profile._meta.get_field('optimal_revenue_per_user').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        traffic = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:organicSearches'}],
                        "dimensions": [{"name": "ga:month"}],
                    }]
            }
        ).execute()
        # print ('Traffic ..................',traffic)
        # print('')

        for current_montn_traffic in traffic['reports']:
            # print ('traffic current month..............',current_montn_traffic['data']['rows'])
            for dimension in current_montn_traffic['data']['rows']:
                pass
                # print ('Dimension................',dimension['dimensions'])

            # print max(int(d) for d in dimension['dimensions'])
            a = max(int(d) for d in dimension['dimensions'])
            for traffic in current_montn_traffic['data']['totals']:
                traffic_vals = cart_rate['values']
                # Profile._meta.get_field('optimal_traffic').default = float(traffic_vals[0])

        # Analytics matrics of Traffic This Month
        traffic_this_month = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
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
        # print ('Traffic this month..................',traffic_this_month)
        # print('')

        for cttm in traffic_this_month['reports']:
            for traffic in cttm['data']['totals']:
                traffic_this_vals = traffic['values']
                # Profile._meta.get_field('traffic_this_month').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        # Analytics matrics of Traffic Last Month
        traffic_last_month = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:organicSearches'}],
                        # "dimensions":[{"name":"ga:month"}],
                    }
                ]
            }
        ).execute()
        # print ('Traffic Last month..................',traffic_last_month)
        # print('')

        for ctlm in traffic_last_month['reports']:
            for traffic_last in ctlm['data']['totals']:
                traffic_last_vals = traffic_last['values']
                # Profile._meta.get_field('traffic_last_month').default = float(last_vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        # Analytics matrics of Revenue This Month
        revenue_this_month = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                        'metrics': [{'expression': 'ga:transactionRevenue'}],
                        "dimensions": [{"name": "ga:month"}],
                    }]
            }
        ).execute()
        # print ('revenue this month..................',revenue_this_month)
        # print('')

        for crtm in revenue_this_month['reports']:
            for revenue in crtm['data']['totals']:
                revenue_this_vals = revenue['values']
                # Profile._meta.get_field('revenue_this_month').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        # Analytics matrics of Revenue Last Month
        revenue_last_month = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
                        'dateRanges': [{'startDate': '60daysAgo', 'endDate': '30daysago'}],
                        'metrics': [{'expression': 'ga:transactionRevenue'}],
                        # "dimensions":[{"name":"ga:month"}],
                    }]
            }
        ).execute()
        # print ('revenue Last Month ..................',revenue_last_month)
        # print('')

        for crlm in revenue_last_month['reports']:
            for revenue in crlm['data']['totals']:
                revenue_last_vals = revenue['values']
                # Profile._meta.get_field('revenue_last_month').default = float(vals[0])
    except:
        raise Exception('Permission Denied')

    try:
        optimal_revenue = service.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '132141628',
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
        raise Exception('Permission Denied')

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
                                    connected=1,
                                    # current_guide_id = guide,
                                    # current_step_id = steps,
                                    # current_task_id = tasks
                                    )
        pr.save()
        pr.update(connected=True)
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
            user_id=user,
            connected=True,
            # current_guide_id = guide,
            # current_step_id = steps,
            # current_task_id = tasks
        )

    return render(request, 'settings/settings.html')


@login_required(login_url='/login/')
def GoogleAuthDisconnect(request):
    # print 'Hello............................'
    Profile.objects.filter(user_id=request.user.id).update(connected=False)
    import os
    os.remove('analytics_%s' % request.user.id + '.dat')
    profile = Profile.objects.filter(user_id=request.user.id).first()
    # print profile.connected
    return render(request, 'settings/settings.html', {'profile': profile})
