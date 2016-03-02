# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0005_auto_20151222_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pool',
            name='data',
        ),
        migrations.RemoveField(
            model_name='project',
            name='data',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='data',
        ),
    ]
