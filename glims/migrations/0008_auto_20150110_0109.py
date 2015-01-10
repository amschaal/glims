# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0007_auto_20150109_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='workflow',
            field=models.ForeignKey(related_name='processes', to='glims.Workflow'),
            preserve_default=True,
        ),
    ]
