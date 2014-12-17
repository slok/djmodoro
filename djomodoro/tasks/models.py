from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Task(models.Model):
    name = models.CharField(_("task name"), max_length=200, null=False)
    description = models.TextField(_("task description"), blank=True)
    # run_set

    def __str__(self):
        return self.name


class Run(models.Model):
    task = models.ForeignKey(Task)
    start = models.DateTimeField(_("Task start time"))
    finish = models.DateTimeField(_("Task finish time"), null=True)

    def clean(self):
        if self.start > self.finish:
            raise ValidationError(
                {'finish': _('Finish time should be older than start time')}
            )

    def __str__(self):
        return "'{0}' task, '{1}' started, '{2}'' finished".format(self.task,
                                                                   self.start,
                                                                   self.finish)
