# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0003_auto_20161110_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='D1MiniCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeviceMACID', models.CharField(max_length=18)),
                ('PinID', models.IntegerField()),
                ('PinMode', models.SmallIntegerField(choices=[('0', 'Input'), ('1', 'Output')])),
                ('PinLevel', models.SmallIntegerField(choices=[('1', 'High'), ('0', 'Low')])),
                ('DateCommand', models.DateTimeField(auto_now=True, null=True)),
                ('Acknowledged', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='D1MiniEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeviceMACID', models.CharField(max_length=18)),
                ('PinID', models.IntegerField()),
                ('PinMode', models.SmallIntegerField(choices=[('0', 'Input'), ('1', 'Output')])),
                ('DateCommand', models.DateTimeField(auto_now=True, null=True)),
                ('Acknowledged', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='d1mini',
            name='BuildInLedLevel',
        ),
        migrations.AddField(
            model_name='d1mini',
            name='BuiltInLedLevel',
            field=models.CharField(choices=[('1', 'High'), ('0', 'Low')], default='L', max_length=1),
        ),
    ]