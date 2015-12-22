# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '0001_initial'),
        ('glims', '0002_status_statusoptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('model_type', models.ForeignKey(to='extensible.ModelType')),
                ('status', models.ForeignKey(related_name='status_options', to='glims.Status')),
            ],
        ),
        migrations.RemoveField(
            model_name='statusoptions',
            name='model_type',
        ),
        migrations.RemoveField(
            model_name='statusoptions',
            name='status',
        ),
        migrations.DeleteModel(
            name='StatusOptions',
        ),
    ]
