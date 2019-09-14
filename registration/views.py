from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from analytics.models import Profile
from sb_mail.models import sbmail_template, sb_settings, mail_message
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from pinax.referrals.models import Referral, ReferralResponse
from .signals import create_user_referral
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .forms import ValidateEmail
from django.template import Template, Context
from django.contrib.auth.decorators import user_passes_test
from sb_shortlink.models import shortlink
# from settings.views import settings,GoogleAuth
import argparse
import webbrowser
import httplib2

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import flow_from_clientsecrets

from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError, OAuth2WebServerFlow
from oauth2client import client, file, tools
from django.contrib.auth.decorators import login_required
from oauth2client.client import AccessTokenRefreshError, AccessTokenCredentials, OAuth2WebServerFlow, OAuth2Credentials, \
    GoogleCredentials, Credentials
import jsonpickle


# Create your views here.
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('/login/')


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'registration/login.html', {'error_message': 'User Does Not Exist'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                sb = sb_settings.objects.first()
                group_names = [x.name for x in sb.signup_group.all()]

                x = lambda u: u.groups.filter(name__in=group_names).count() > 0
                if x(user) == True:
                    return redirect('/thankyou/')
                else:
                    profile = Profile.objects.filter(user_id=request.user.id).first()
                    if profile and profile.google_authcode:
                        analytics_job(request)
                    return redirect('/taskoftheday/start')
            else:
                return render(request, 'registration/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid Username Or Password'})
    return render(request, 'registration/login.html')


@csrf_exempt
def register(request):
    form = UserForm(request.POST or None)
    username = request.POST.get('username')

    # x = sbmail_template.objects.filter(id=3).get()
    # print x
    priority = 'Urgent'
    context = {'priority': priority}
    # profiles = Profile.objects.all()
    # for profile in profiles:
    # print x.send(187,context)

    # template = sbmail_template.objects.filter(id=1).get()
    # data =  template.body_html
    # if template and template.object:
    #     __model =  globals()[template.object]
    #     obj = __model.objects.get(id=29)

    #     if obj:
    #         t = Template( template.body_html if template and template.body_html else  '' )
    #         c = Context(  {"object": obj}    if template and template.body_html else  {} )
    #         html_code = t.render(c)
    #         print html_code
    if form.is_valid():

        if ValidateEmail(username) is False:
            context = {
                "form": form,
                'username': username,
                'user_errormessage': 'Enter Valid User Name as email'
            }
            return render(request, 'registration/register.html', context)
        else:
            # for getting referralcode
            referralcode = request.POST['referralcode']
            username = request.POST['username']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            if password != password_confirm:
                context = {
                    "form": form,
                    'username': username,
                    'password_errormessage': 'your password doesnot match . '
                }
                return render(request, 'registration/register.html', context)

            # for getting ip address      
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

            # ref : instance if match referencecode.
            ref = Referral.objects.filter(code=referralcode).first()

            if referralcode != '' and not ref:
                context = {
                    "form": form,
                    'username': username,
                    'error_message1': 'Wrong Referral Code.Please enter correct referral code or to signup without referral, leave the blank referral'
                }
                return render(request, 'registration/register.html', context)
            else:
                user = form.save(commit=False)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                sb = sb_settings.objects.first()
                group_names = [x.name for x in sb.signup_group.all()]

                for g in sb.signup_group.all():
                    g.user_set.add(user)

                post_save.connect(create_user_referral, sender=User)
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    # pro = Profile.objects.all().last()
                    new_ref = Profile.objects.create(user_id=user, current_user_name=user.username, rank=sb.rank)
                    sb_settings.objects.filter(id=sb.id).update(rank=F('rank') + 1)

                    login(request, user)

                    if referralcode != '' and ref and referralcode == ref.code:
                        if not request.session.session_key:
                            request.session.save()
                        session = request.session.session_key
                        Profile.objects.filter(user_id=ref.user).update(profilerank=F('profilerank') + 1)
                        # CREATE REFERRAL RESPONSE, IN RESPECT TO REFERRAL CODE
                        ReferralResponse.objects.create(user=user, referral=ref, ip_address=ip, session_key=session)
                    x = lambda u: u.groups.filter(name__in=group_names).count() > 0

                    ref1 = Referral.objects.filter(user=user).first()

                    link = 'registration/register/?referral_code=%s' % ref1.code
                    url1 = shortlink(url=link)
                    short = shortlink.shorten(url1)
                    realurl = '%s://%s/%s' % (request.scheme, request.META['HTTP_HOST'], link)

                    slink = shortlink.objects.create(short=short, url=realurl, active=user.is_active, user=user)
                    Profile.objects.filter(user_id=user).update(profilelink=slink)

                    if x(user) == True:
                        return redirect('/thankyou/')
                    else:
                        return redirect('/taskoftheday/start')

    if username:
        context = {
            "form": form,
            'username': username,
            'user_errormessage': 'Enter valid username'
        }
        return render(request, 'registration/register.html', context)

    context = {
        "form": form,
        'referral_code': request.GET.get('referral_code', '')

    }

    return render(request, 'registration/register.html', context)


@login_required(login_url='/login/')
def analytics_job(request):
    profile1 = Profile.objects.filter(user_id=request.user.id).first()
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
        # credentials = GoogleCredentials.get_application_default()
        # credentials = OAuth2Credentials.get_access_token()
        # credentials = AccessTokenCredentials(access_token,'my-user-agent/1.0')
        # if credentials.access_token_expired:
        #    http_auth = credentials.authorize(httplib2.Http())
        # else:
        #    print "1"
        credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, token_expiry, token_uri,
                                        'my-user-agent/1.0', revoke_uri)
        http_auth = credentials.authorize(httplib2.Http())
        # http_auth = credentials.refresh(httplib2.Http())
        # print '@@@',credentials.access_token_expired
        # credentials = credentials.refresh(credentials)
        # print credentials
        # if credentials.access_token_expired:
        #     print credentials.refresh(http_auth)
        # if credentials.access_token_expired:
        #     http_auth = credentials.authorize(httplib2.Http())
        # else:
        #     print 'not expired'
        #     #http_auth = credentials.authorize(httplib2.Http())
        #     refresh = credentials.refresh(httplib2.Http())
        #     print jsonpickle.encode(refresh)
        #     print refresh
        service = build('analytics', 'v3', http_auth, cache_discovery=False)

        # accounts = service.management().accounts().list().execute()
        # if accounts.get('items'):
        #     account = accounts.get('items')[0].get('id')

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
                            'viewId': profile,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:goalConversionRateAll'}]
                        }]
                }
            ).execute()

            for ccr in conversion_rate['reports']:
                for rate in ccr['data']['totals']:
                    conversion_vals = rate['values']
        except:
            conversion_vals = [0]
            pass

        try:
            bounce_rate = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:bounceRate'}]
                        }]
                }
            ).execute()

            for cbr in bounce_rate['reports']:
                for rate in cbr['data']['totals']:
                    bounce_vals = rate['values']

        except:
            bounce_vals = [0]
            pass
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
                            'viewId': profile,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [metric_expression],
                        }]
                }
            ).execute()

            for caov in avg_order_value['reports']:
                for order in caov['data']['totals']:
                    order_value = order['values']

        except:
            order_value = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            cart_abandonment_rate = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:goalAbandonRateAll'}],
                        }]
                }
            ).execute()

            for ccar in cart_abandonment_rate['reports']:
                for cart_rate in ccar['data']['totals']:
                    cart_vals = cart_rate['values']

        except:
            cart_vals = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            revenue_per_user = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '100daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:revenuePerUser'}],
                            # "dimensions":[{"name":"ga:transactionId"}],
                        }]
                }
            ).execute()

            for crpu in revenue_per_user['reports']:
                for revenue in crpu['data']['totals']:
                    revenue_vals = revenue['values']

        except:
            revenue_vals = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            traffic = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
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

            # Analytics matrics of Traffic This Month
            traffic_this_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
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

        except:
            traffic_this_vals = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            # Analytics matrics of Traffic Last Month
            traffic_last_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
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

        except:
            traffic_last_vals = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            # Analytics matrics of Revenue This Month
            revenue_this_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            "dimensions": [{"name": "ga:month"}],
                        }]
                }
            ).execute()

            for crtm in revenue_this_month['reports']:
                for revenue in crtm['data']['totals']:
                    revenue_this_vals = revenue['values']

        except:
            raise Exception('Permission Denied')

        try:
            # Analytics matrics of Revenue Last Month
            revenue_last_month = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '60daysAgo', 'endDate': '30daysago'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            # "dimensions":[{"name":"ga:month"}],
                        }]
                }
            ).execute()

            for crlm in revenue_last_month['reports']:
                for revenue in crlm['data']['totals']:
                    revenue_last_vals = revenue['values']

        except:
            revenue_last_vals = [0]
            pass
            # raise Exception('Permission Denied')

        try:
            optimal_revenue = service.reports().batchGet(
                body={
                    'reportRequests': [
                        {
                            'viewId': profile,
                            'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                            'metrics': [{'expression': 'ga:transactionRevenue'}],
                            # "dimensions":[{"name":"ga:month"}],
                        }]
                }
            ).execute()

            for optrev in optimal_revenue['reports']:
                for revenue in optrev['data']['totals']:
                    optimal_revenue_vals = revenue['values']

        except:
            optimal_revenue_vals = [0]
            pass
            # raise Exception('Permission Denied')

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
    return 1
