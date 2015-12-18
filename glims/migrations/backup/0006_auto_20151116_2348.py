# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0005_project_project_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='sample_prefix',
        ),
        migrations.RemoveField(
            model_name='project',
            name='slug',
        ),
    ]
