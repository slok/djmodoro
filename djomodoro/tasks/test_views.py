from datetime import timedelta
import math

from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import timezone

from .models import Task, Run


@override_settings(DEBUG=True)  # For the static ones
class TestTasks(TestCase):

    def setUp(self):
        self.tasks = (
            {
                'name': "Task one",
                'description': "Do task one"
            },
            {
                'name': "Task two",
                'description': "Do task two"
            }
        )

        self.runs = (
            {
                "task_id": 1,
                "start": timezone.now(),
                "finish": timezone.now() + timedelta(hours=2)
            },
            {
                "task_id": 2,
                "start": timezone.now(),
                "finish": timezone.now() + timedelta(minutes=1)
            },
            {
                "task_id": 2,
                "start": timezone.now(),
                "finish": timezone.now() + timedelta(minutes=43)
            },
            {
                "task_id": 2,
                "start": timezone.now(),
                "finish": timezone.now() + timedelta(hours=2)
            },
        )

    def test_create_task(self):
        url = reverse("tasks:task_create")
        c = Client()

        for i in self.tasks:
            response = c.post(url, i)

            self.assertRedirects(response, url)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                Task.objects.filter(
                    name=i['name'])[0].description, i['description'])

        self.assertEqual(Task.objects.count(), len(self.tasks))

    def test_detail_task(self):

        tasks = []
        c = Client()

        for i in self.tasks:
            t = Task(name=i['name'], description=i['description'])
            t.save()
            tasks.append(t)

        for i in self.runs:
            t = Task.objects.get(id=i['task_id'])
            Run(task=t, start=i['start'], finish=i['finish']).save()

        for i in self.tasks:
            t = Task.objects.get(name=i['name'])
            url = reverse("tasks:task_detail", kwargs={'pk': t.id})
            response = c.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['task_object'],
                             Task.objects.get(id=t.id))

            self.assertEqual(
                len(response.context['run_list']), t.run_set.count())

    def test_detail_task_pagination(self):

        # Populate database
        runs_quantity = 23
        paginate_by = 10

        t = Task(name="pagination task", description="pagination task desc")
        t.save()

        for i in range(runs_quantity):
            Run(task=t, start=timezone.now(), finish=timezone.now()).save()

        c = Client()
        url_fmt = "{0}?page={1}"

        # Per page
        i = 0
        while True:
            i += 1  # Page counter
            url = reverse("tasks:task_detail", kwargs={'pk': t.id})
            url = url_fmt.format(url, i)
            response = c.get(url)
            list_count = response.context['run_list'].count()

            if response.context['page_obj']['has_next']:
                self.assertEqual(list_count, paginate_by)
            else:  # Last case
                self.assertEqual(list_count, runs_quantity % paginate_by)
                break

#class TestTasks(TestCase):
#        def test_index_200():
#            c = Client()
#            response = c.post('/login/', {'username': 'john', 'password': 'smith'})
#            response.status_code
#
#            response = c.get('/customer/details/')
#            response.content