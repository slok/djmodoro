from django.test import TestCase

from .models import Task


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

    def test_save(self):
        """Save task object"""
        for i in self.data:
            t = Task(name=i['name'], description=i['description'])
            t.save()

        self.assertEqual(Task.objects.count(), len(self.data))

    def test_retrieve(self):
        """retrieve task object"""
        for i in self.data:
            t = Task(name=i['name'], description=i['description'])
            t.save()

        tasks = Task.objects.all().order_by("id")

        for i, v in enumerate(self.data):
            self.assertEqual(tasks[i].name, v['name'])
            self.assertEqual(tasks[i].description, v['description'])

    def test_update(self):
        """update task object"""
        for i in self.data:
            t = Task(name=i['name'], description=i['description'])
            t.save()

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
        for i in self.data:
            t = Task(name=i['name'], description=i['description'])
            t.save()

        # Update
        for i in Task.objects.all().order_by("id"):
            i.delete()

        self.assertEqual(Task.objects.count(), 0)
