# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='d1mini',
            name='LastHeard',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
