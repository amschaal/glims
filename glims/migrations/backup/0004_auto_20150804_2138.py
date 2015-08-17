# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '__first__'),
        ('glims', '0003_remove_modeltype_form_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='modeltype',
            name='plugins',
        ),
        migrations.AddField(
            model_name='plugin',
            name='model_types',
            field=models.ManyToManyField(related_name='plugins', null=True, through='glims.ModelTypePlugins', to='extensible.ModelType', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modeltypeplugins',
            name='type',
            field=models.ForeignKey(to='extensible.ModelType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pool',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='process',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sample',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workflow',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='ModelType',
        ),
        migrations.AlterField(
            model_name='workflowprocess',
            name='process',
            field=models.ForeignKey(related_name='+', to='extensible.ModelType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workflowtemplate',
            name='processes',
            field=models.ManyToManyField(related_name='+', through='glims.WorkflowProcess', to='extensible.ModelType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workflowtemplate',
            name='type',
            field=models.ForeignKey(related_name='+', to='extensible.ModelType'),
            preserve_default=True,
        ),
    ]
