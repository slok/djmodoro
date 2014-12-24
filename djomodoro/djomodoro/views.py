from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy


class IndexRedirect(RedirectView):
    def get_redirect_url(self):
        return reverse_lazy("tasks:index")
