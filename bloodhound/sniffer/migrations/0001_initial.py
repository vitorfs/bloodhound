# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlFrontier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sniff_session', models.UUIDField()),
                ('url', models.URLField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_visited', models.BooleanField(default=False)),
                ('visited_at', models.DateTimeField(null=True)),
                ('status_code', models.IntegerField(null=True)),
            ],
        ),
    ]
