from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from tasks import urls as task_urls

urlpatterns = patterns('',
    url(r'^t/', include(task_urls, namespace="tasks")),
    url(r'^admin/', include(admin.site.urls)),
)

# Django debug toolbar stuff
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
