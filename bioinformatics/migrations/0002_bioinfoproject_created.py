# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bioinformatics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bioinfoproject',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 22, 21, 56, 54, 586192, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
