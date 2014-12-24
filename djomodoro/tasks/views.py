from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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
        response = super().form_valid(form)
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
    success_url = reverse_lazy("tasks:index")


class UpdateRunView(AjaxableResponseMixin, UpdateView):
    model = Run
    fields = ['task', 'start', 'finish']
    template_name = "tasks/task_index.html"

    def get_success_url(self):
        return reverse_lazy("tasks:run_update", kwargs=self.kwargs)


class RunListView(ListView):
    queryset = Run.objects.order_by('-id')
    template_name = "tasks/task_run_list.html"
    context_object_name = "run_list"
    paginate_by = 10


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


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_task_detail.html"
    context_object_name = "task_object"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = self.__class__.paginate_by
        # Add our custom paginator
        page = int(self.request.GET.get('page', 1))

        run_list_count = Run.objects.filter(task_id=self.kwargs['pk']).count()
        context['run_list'] = Run.objects.filter(
            task_id=self.kwargs['pk'])[(page-1)*paginate_by:page*paginate_by]

        context['is_paginated'] = run_list_count > 0
        if context['is_paginated']:
            page_obj = {
                'has_previous': page > 1,
                'has_next': (run_list_count - (page * paginate_by)) > 0,
                'previous_page_number': page - 1,
                'next_page_number': page + 1,
            }
            context['page_obj'] = page_obj
        return context
