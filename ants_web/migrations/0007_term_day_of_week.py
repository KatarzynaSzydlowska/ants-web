# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ants_web', '0006_auto_20161205_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='day_of_week',
            field=models.CharField(default='M', max_length=1),
            preserve_default=False,
        ),
    ]