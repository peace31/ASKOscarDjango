from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
@login_required(login_url='/login/')
# @user_passes_test(lambda u: u.groups.filter(name='email_subscribed').count() == 0, login_url='/login/')
def analytics(request):
    obj = Profile.objects.filter(user_id=request.user.id).first()
    print ('Obj.............', obj)
    return render(request, 'analytics/analytics.html', {'obj': obj})
