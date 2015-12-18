# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_cloudstore', '0001_initial'),
        ('glims', '0006_auto_20151116_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='cloudstore',
            field=models.ForeignKey(blank=True, to='django_cloudstore.CloudStore', null=True),
            preserve_default=True,
        ),
    ]
