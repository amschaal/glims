# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0002_project_sample_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='slug',
            field=models.SlugField(max_length=20, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='sample_prefix',
            field=models.CharField(max_length=5, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=25, null=True),
            preserve_default=True,
        ),
    ]
