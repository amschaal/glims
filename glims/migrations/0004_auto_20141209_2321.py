# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0003_auto_20141209_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='type',
            field=models.ForeignKey(blank=True, to='glims.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, to='glims.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sample',
            name='type',
            field=models.ForeignKey(blank=True, to='glims.ModelType', null=True),
            preserve_default=True,
        ),
    ]
