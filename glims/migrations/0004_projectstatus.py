# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('glims', '0003_auto_20151221_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(related_name='statuses', to='glims.Project')),
                ('set_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(to='glims.Status')),
            ],
        ),
    ]
