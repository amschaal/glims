# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_json_forms', '0001_initial'),
        ('glims', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SLURM',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.drmaajob',),
        ),
        migrations.AddField(
            model_name='modeltype',
            name='form_model',
            field=models.ForeignKey(blank=True, to='django_json_forms.JSONFormModel', null=True),
            preserve_default=True,
        ),
    ]
