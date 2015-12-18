# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0008_auto_20151117_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='type',
        ),
        migrations.RemoveField(
            model_name='process',
            name='workflow',
        ),
        migrations.DeleteModel(
            name='Process',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='pool',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='samples',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='type',
        ),
        migrations.RemoveField(
            model_name='workflow',
            name='workflow_template',
        ),
        migrations.DeleteModel(
            name='Workflow',
        ),
        migrations.RemoveField(
            model_name='workflowprocess',
            name='process',
        ),
        migrations.RemoveField(
            model_name='workflowprocess',
            name='workflow',
        ),
        migrations.RemoveField(
            model_name='workflowtemplate',
            name='processes',
        ),
        migrations.DeleteModel(
            name='WorkflowProcess',
        ),
        migrations.RemoveField(
            model_name='workflowtemplate',
            name='type',
        ),
        migrations.DeleteModel(
            name='WorkflowTemplate',
        ),
    ]
