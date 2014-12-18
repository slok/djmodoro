from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^task/create$', views.NewTaskView.as_view(), name="task_create"),
    #url(r'^$', views.IndexView.as_view(), name="list-tasks"),
    #url(r'^$', views.IndexView.as_view(), name="list-runs"),
)
