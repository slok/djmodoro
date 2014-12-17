from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Task, Run


# Simple tests, this shouldn't be neccessary, the ORM is already tested
# by Django :P
class TaskTestCase(TestCase):

    def setUp(self):
        self.data = [
            {
                "name": "Develop Djomodoro",
                "description": "Develop a pomodoro clone in Django"
            },
            {
                "name": "Delete app",
                "description": "Delete random rails app"
            },
            {
                "name": "Install GNU/Linux",
                "description": "Install GNU/Linux on some Windows machines"
            }
        ]
        for i in self.data:
            t = Task(name=i['name'], description=i['description'])
            t.save()

    def test_save(self):
        """Save task object"""
        self.assertEqual(Task.objects.count(), len(self.data))

    def test_retrieve(self):
        """retrieve task object"""
        tasks = Task.objects.all().order_by("id")

        for i, v in enumerate(self.data):
            self.assertEqual(tasks[i].name, v['name'])
            self.assertEqual(tasks[i].description, v['description'])

    def test_update(self):
        """update task object"""
        # Update
        for i in Task.objects.all().order_by("id"):
            i.name += "_updated"
            i.save()

        tasks = Task.objects.all().order_by("id")

        for i, v in enumerate(self.data):
            self.assertEqual(tasks[i].name, v['name'] + "_updated")
            self.assertEqual(tasks[i].description, v['description'])

    def test_delete(self):
        """delete task object"""
        for i in Task.objects.all():
            i.delete()

        self.assertEqual(Task.objects.count(), 0)


class RunTestCase(TestCase):

    def setUp(self):
        self.tasks = [
            {
                "name": "Develop Djomodoro",
                "description": "Develop a pomodoro clone in Django"
            },
            {
                "name": "Delete app",
                "description": "Delete random rails app"
            },
            {
                "name": "Install GNU/Linux",
                "description": "Install GNU/Linux on some Windows machines"
            }
        ]

        for i in self.tasks:
            Task(name=i['name'], description=i['description']).save()

        self.runs = [
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
                "task_id": 3,
                "start": timezone.now(),
                "finish": timezone.now() + timedelta(minutes=43)
            },
        ]
        for i in self.runs:
            Run(task=Task.objects.get(id=i['task_id']), start=i['start'],
                finish=i['finish']).save()

    def test_save(self):
        """Save run object"""
        self.assertEqual(Run.objects.count(), len(self.runs))

    def test_retrieve(self):
        """retrieve run object"""
        runs = Run.objects.all()

        for i, v in enumerate(self.runs):
            self.assertEqual(runs[i].task, Task.objects.get(id=v['task_id']))
            self.assertEqual(runs[i].start, v['start'])
            self.assertEqual(runs[i].finish, v['finish'])

    def test_update(self):
        """update update object"""
        # Update
        now = timezone.now() - timedelta(hours=5, minutes=4, seconds=23)
        for i in Run.objects.all():
            i.start = now
            i.save()

        runs = Run.objects.all().order_by("id")

        for i, v in enumerate(self.runs):
            self.assertEqual(runs[i].task, Task.objects.get(id=v['task_id']))
            self.assertEqual(runs[i].start, now)
            self.assertEqual(runs[i].finish, v['finish'])

    def test_delete(self):
        """delete runs object"""
        for i in Run.objects.all():
            i.delete()

        self.assertEqual(Run.objects.count(), 0)

    def test_finish_validation(self):
        """test finish field validation"""
        t = Task.objects.get(id=1)
        now = timezone.now()

        r_now = Run(task=t, start=now, finish=now)
        r_future = Run(task=t, start=now, finish=(now + timedelta(seconds=1)))
        r_past = Run(task=t, start=now, finish=(now - timedelta(seconds=1)))

        r_now.full_clean()
        r_future.full_clean()

        with self.assertRaises(ValidationError):
            r_past.full_clean()
