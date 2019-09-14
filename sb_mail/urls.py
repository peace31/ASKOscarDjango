from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.settings),
    url(r'test', views.mails),

]
