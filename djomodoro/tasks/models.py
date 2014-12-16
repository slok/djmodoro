from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Task(models.Model):
    name = models.CharField(_("task name"), max_length=200, null=False)
    description = models.TextField(_("task description"), blank=True)

    def __str__(self):
        return self.name
