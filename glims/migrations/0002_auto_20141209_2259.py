# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttype',
            name='plugins',
        ),
        migrations.RemoveField(
            model_name='projecttypeplugins',
            name='plugin',
        ),
        migrations.RemoveField(
            model_name='projecttypeplugins',
            name='type',
        ),
        migrations.DeleteModel(
            name='ProjectTypePlugins',
        ),
        migrations.AddField(
            model_name='experiment',
            name='data',
            field=django_hstore.fields.DictionaryField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='refs',
            field=django_hstore.fields.ReferencesField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experiment',
            name='type',
            field=models.ForeignKey(default=None, to='glims.ModelType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='data',
            field=django_hstore.fields.DictionaryField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='refs',
            field=django_hstore.fields.ReferencesField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.ForeignKey(to='glims.ModelType'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ProjectType',
        ),
    ]
