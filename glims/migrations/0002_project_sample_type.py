# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '0001_initial'),
        ('glims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sample_type',
            field=models.ForeignKey(related_name='+', blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
    ]
