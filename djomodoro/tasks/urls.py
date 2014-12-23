from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^task/create$', views.NewTaskView.as_view(), name="task_create"),
    url(r'^run/update/(?P<pk>\d+)$', views.UpdateRunView.as_view(),
        name="run_update"),
    url(r'^run/list$', views.RunListView.as_view(), name="run_list"),
    #url(r'^run/create$', views.NewRunView.as_view(), name="run_create"),
    #url(r'^$', views.IndexView.as_view(), name="list-tasks"),
)
