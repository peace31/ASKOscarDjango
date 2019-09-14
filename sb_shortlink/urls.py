from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(.*)$', views.verifyurl),
    # url(r'^(?P[0-9a-zA-Z]+)/', views.verifyurl),

]
