# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0002_auto_20141209_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelTypePlugins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('layout', models.CharField(max_length=10, choices=[(b'inline', b'Inline'), (b'tabbed', b'Tab')])),
                ('header', models.CharField(max_length=30, null=True, blank=True)),
                ('plugin', models.ForeignKey(to='glims.Plugin')),
                ('type', models.ForeignKey(to='glims.ModelType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='modeltype',
            name='plugins',
            field=models.ManyToManyField(to='glims.Plugin', null=True, through='glims.ModelTypePlugins', blank=True),
            preserve_default=True,
        ),
    ]
