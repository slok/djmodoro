from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^run/update/(?P<pk>\d+)$', views.UpdateRunView.as_view(),
        name="run_update"),
    url(r'^run/list$', views.RunListView.as_view(), name="run_list"),
    url(r'^task/create$', views.NewTaskView.as_view(), name="task_create"),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(),
        name="task_detail"),
)
