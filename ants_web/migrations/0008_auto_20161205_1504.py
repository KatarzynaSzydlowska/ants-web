# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ants_web', '0007_term_day_of_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='day_of_week',
            field=models.CharField(max_length=2),
        ),
    ]