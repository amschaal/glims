# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0004_auto_20141209_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeltype',
            name='schema',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
    ]
