# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import glims.lims
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailRecipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=75)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('email', models.ForeignKey(related_name='recipients', to='glims.Email')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.CharField(default=glims.lims.generate_pk, max_length=30, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'permissions': (('view', 'View Experiment'), ('admin', 'Administer Experiment')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=50, null=True, blank=True)),
                ('path', models.CharField(max_length=250)),
                ('job_id', models.CharField(max_length=30, null=True, blank=True)),
                ('_args', models.TextField(null=True, blank=True)),
                ('_config', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('app', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('page', models.CharField(max_length=50)),
                ('template', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(default=glims.lims.generate_pk, max_length=20, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
            options={
                'permissions': (('view', 'View Project'), ('admin', 'Administer Project'), ('pi', 'Can PI a Project')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectTypePlugins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('layout', models.CharField(max_length=10, choices=[(b'inline', b'Inline'), (b'tabbed', b'Tab')])),
                ('header', models.CharField(max_length=30, null=True, blank=True)),
                ('plugin', models.ForeignKey(to='glims.Plugin')),
                ('type', models.ForeignKey(to='glims.ProjectType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', django_hstore.fields.DictionaryField()),
                ('refs', django_hstore.fields.ReferencesField()),
                ('sample_id', models.CharField(unique=True, max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('received', models.DateField(null=True, blank=True)),
                ('project', models.ForeignKey(related_name='samples', to='glims.Project')),
                ('type', models.ForeignKey(to='glims.ModelType')),
            ],
            options={
                'permissions': (('view', 'View Sample'), ('admin', 'Administer Sample')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projecttype',
            name='plugins',
            field=models.ManyToManyField(to='glims.Plugin', null=True, through='glims.ProjectTypePlugins', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.ForeignKey(to='glims.ProjectType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='experiment',
            name='sample',
            field=models.ForeignKey(related_name='experiments', to='glims.Sample'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ClusterJob',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.job',),
        ),
        migrations.CreateModel(
            name='DRMAAJob',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.job',),
        ),
        migrations.CreateModel(
            name='SGE',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.drmaajob',),
        ),
    ]
