# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 12:47
from __future__ import unicode_literals

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ants_web', '0002_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kind', models.CharField(max_length=8)),
                ('starts_at', models.TimeField()),
                ('ends_at', models.TimeField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='course',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='term',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ants_web.Course'),
        ),
        migrations.AddField(
            model_name='term',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ants_web.Instructor'),
        ),
        migrations.AddField(
            model_name='term',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ants_web.Location'),
        ),
    ]