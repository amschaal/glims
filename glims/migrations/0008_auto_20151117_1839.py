# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0007_lab_cloudstore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='cloudstore',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='django_cloudstore.CloudStore', null=True),
            preserve_default=True,
        ),
    ]
