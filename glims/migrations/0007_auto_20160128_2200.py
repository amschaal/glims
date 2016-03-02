# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0006_auto_20160128_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='data',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={}, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='data',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={}, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='data',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={}, null=True, blank=True),
        ),
    ]
