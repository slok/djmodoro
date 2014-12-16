# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='task name', max_length=200)),
                ('description', models.TextField(verbose_name='task description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
