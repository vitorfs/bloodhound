# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('url', models.URLField(max_length=1000, null=True, blank=True)),
                ('status', models.CharField(default='NEW', max_length=10, choices=[('NEW', 'New'), ('OK', 'Ok'), ('ERROR', 'Error'), ('NOT_FOUND', 'Not found')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('visited_at', models.DateTimeField(auto_now=True)),
                ('current_price', models.FloatField(null=True)),
                ('last_price', models.FloatField(null=True)),
                ('price_raw_variance', models.FloatField(null=True)),
                ('price_percentage_variance', models.FloatField(default=0.0)),
                ('price_changes', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='product',
            field=models.ForeignKey(related_name='price_history', to='core.Product'),
        ),
    ]
