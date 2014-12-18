from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from .models import Task


class IndexView(TemplateView):
    template_name = "tasks/task_index.html"


class NewTaskView(SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'description']
    template_name = "tasks/task_task_create.html"
    success_url = reverse_lazy("tasks:task_create")
    success_message = _("%(name)s was created successfully")

    def get_context_data(self, **kwargs):
        kwargs['task_list'] = Task.objects.annotate(
                                Count('run')).order_by('-id')[:5]
        return super().get_context_data(**kwargs)  # Python3 style super
