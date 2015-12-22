# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0004_projectstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectstatus',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectstatus',
            name='set_by',
        ),
        migrations.RemoveField(
            model_name='projectstatus',
            name='status',
        ),
        migrations.AddField(
            model_name='project',
            name='history',
            field=jsonfield.fields.JSONField(default={}, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(blank=True, to='glims.Status', null=True),
        ),
        migrations.AlterField(
            model_name='statusoption',
            name='model_type',
            field=models.ForeignKey(related_name='status_options', to='extensible.ModelType'),
        ),
        migrations.AlterField(
            model_name='statusoption',
            name='status',
            field=models.ForeignKey(to='glims.Status'),
        ),
        migrations.DeleteModel(
            name='ProjectStatus',
        ),
    ]
