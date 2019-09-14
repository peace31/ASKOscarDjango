from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.settings),
    url(r'googleauth', views.GoogleAuth),
    url(r'disconnect', views.GoogleAuthDisconnect),
    url(r'massreferral', views.massreferral),
    url(r'profile', views.profile),
    url(r'payments', views.payments),
]
