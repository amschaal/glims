# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bioinformatics', '0002_bioinfoproject_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='bioinfoproject',
            name='name',
            field=models.CharField(default='temporary value', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bioinfoproject',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
