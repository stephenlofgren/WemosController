# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 03:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0004_auto_20161113_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='d1minicommand',
            name='DeviceMACID',
        ),
        migrations.RemoveField(
            model_name='d1minievent',
            name='DeviceMACID',
        ),
        migrations.AddField(
            model_name='d1minicommand',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Base.D1Mini'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='d1minievent',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Base.D1Mini'),
            preserve_default=False,
        ),
    ]