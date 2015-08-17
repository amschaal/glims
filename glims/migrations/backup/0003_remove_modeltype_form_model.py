# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0002_auto_20150721_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeltype',
            name='form_model',
        ),
    ]
