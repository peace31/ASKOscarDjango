from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'start$', views.taskoftheday, name="taskoftheday"),
    url(r'^detail_taskoftheday$', views.detail_taskoftheday, name="detail_taskoftheday"),
    url(r'(?P<guide_id>[0-9]+)/(?P<step_id>[0-9]+)/(?P<task_id>[0-9]+)/$', views.detail_taskoftheday,
        name="taskoftheday"),

    # www.askoskar.com/taskoftheday/1/4/3 (1=guide1, 4= step 4, 3=task 3)

]
