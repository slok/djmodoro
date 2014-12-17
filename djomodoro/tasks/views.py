from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "tasks/task_index.html"
