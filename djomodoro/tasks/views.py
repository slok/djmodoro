from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from .models import Task, Run


# Custom mixins
class AjaxableResponseMixin(object):

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class IndexView(AjaxableResponseMixin, CreateView):
    model = Run
    fields = ['task', 'start']
    template_name = "tasks/task_index.html"
    success_url = reverse_lazy("tasks:run_create")


class UpdateRunView(AjaxableResponseMixin, UpdateView):
    model = Run
    fields = ['task', 'start', 'finish']
    template_name = "tasks/task_index.html"

    def get_success_url(self):
        return reverse_lazy("tasks:run_update", kwargs=self.kwargs)


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


class NewRunView(SuccessMessageMixin, CreateView):
    model = Run
    fields = ['task', 'start', 'finish']
    template_name = "tasks/task_run_create.html"
    success_url = reverse_lazy("tasks:run_create")
    success_message = _("task started at %(start)s was created successfully")
