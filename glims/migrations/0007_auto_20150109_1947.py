# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0006_auto_20150109_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processtemplate',
            name='type',
        ),
        migrations.RemoveField(
            model_name='process',
            name='process_template',
        ),
        migrations.RemoveField(
            model_name='workflowtemplate',
            name='process_templates',
        ),
        migrations.AddField(
            model_name='workflowtemplate',
            name='processes',
            field=models.ManyToManyField(related_name='+', through='glims.WorkflowProcess', to='glims.ModelType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modeltype',
            name='schema',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workflowprocess',
            name='process',
            field=models.ForeignKey(related_name='+', to='glims.ModelType'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ProcessTemplate',
        ),
        migrations.AlterField(
            model_name='workflowtemplate',
            name='type',
            field=models.ForeignKey(related_name='+', to='glims.ModelType'),
            preserve_default=True,
        ),
    ]
