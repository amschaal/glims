# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import glims.lims


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0004_auto_20151110_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_id',
            field=models.CharField(default=glims.lims.generate_project_id, max_length=4, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
