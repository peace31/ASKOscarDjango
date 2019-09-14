from django.http import HttpResponse
from django.shortcuts import render, redirect
from sb_mail.models import Email_Subscription
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group

from django.db import IntegrityError
import re
from analytics.models import Profile
from sb_mail.models import sbmail_template, sb_settings
from pinax.referrals.models import Referral
from django.contrib.auth.decorators import login_required
from django.db.models import F
from sb_shortlink.models import shortlink
from django.contrib.auth import login


def landing_page(request):
    return render(request, 'login1.html')


def thanks(request):
    return render(request, 'thank_you.html')


def thanks_again(request):
    return render(request, 'thanks_again.html')


def invalidurl(request):
    return render(request, 'thank_you2.html')


@login_required(login_url='/login/')
def thankyou(request):
    profile = Profile.objects.filter(user_id=request.user.id).first()
    # GET REFERRAL OBJECT OF THIS USER
    referral = Referral.objects.filter(user=request.user).first()
    referralcode = referral.code if referral else None
    url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'], profile.profilelink.short)
    profilerank = profile.profilerank if profile else None

    return render(request, 'thank_you1.html', {'profilerank': profilerank, 'url': url})


@csrf_exempt
def email_subscribe(request):
    name = request.POST['name']
    email = request.POST['email']
    password = User.objects.make_random_password()
    if request.method == "POST":
        Email_Subscription.objects.create(name=name, email=email)

    username = request.POST.get('email')

    _DUPLICATE_USERNAME_ERRORS = (
        'column username is not unique',
        'UNIQUE constraint failed: auth_user.username',
        'duplicate key value violates unique constraint "auth_user_username_key"\n'
    )
    message = "Please Enter Unique Email Address"

    try:
        user = User.objects.create_user(username, email, password)
    except IntegrityError as err:
        regexp = '|'.join(re.escape(e) for e in _DUPLICATE_USERNAME_ERRORS)
        if re.match(regexp, str(err)):
            return render(request, 'landing_index.html', {'message': message})
        raise
    user.save()

    sb = sb_settings.objects.first()
    group_names = [x.name for x in sb.signup_group.all()]

    for g in sb.signup_group.all():
        g.user_set.add(user)

    referral = Referral.objects.filter(user=user).get()
    link = 'registration/register/?referral_code=%s' % referral.code
    url1 = shortlink(url=link)
    short = shortlink.shorten(url1)
    realurl = '%s://%s/%s' % (request.scheme, request.META['HTTP_HOST'], link)
    slink = shortlink.objects.create(short=short, url=realurl, active=user.is_active, user=user)

    sb_rank = sb.rank
    profile = Profile.objects.create(user_id=user, current_user_name=user.username, referral=referral, rank=sb_rank,
                                     profilelink=slink)
    sb_settings.objects.filter(id=sb.id).update(rank=F('rank') + 1)
    url = '%s://%s/i/%s' % (request.scheme, request.META['HTTP_HOST'], profile.profilelink.short)
    x = sbmail_template.objects.filter(id=3).get()
    priority = 'Urgent'
    context = {'password': password, 'url': url, 'priority': priority}
    if x.send(profile.id, context) == 1:
        x = lambda u: u.groups.filter(name__in=group_names).count() > 0
        login(request, user)
        if x(user) == True:
            return redirect('/thankyou/')
        else:
            return redirect('/taskoftheday/start')
    else:
        return render(request, 'landing_index.html', {'message': x.send(profile.id, context)})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'login1.html', {'error_message': 'User Does Not Exist'})
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
                return render(request, 'login1.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login1.html', {'error_message': 'Invalid Username Or Password'})
    return render(request, 'login1.html')
