from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin

from tasks import urls as task_urls

urlpatterns = patterns('',
    url(r'^t/', include(task_urls, namespace="tasks")),
    url(r'^admin/', include(admin.site.urls)),
)

# In production static stuff should be server by http server
# static handles automatically
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django debug toolbar stuff
# Handles static files
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
