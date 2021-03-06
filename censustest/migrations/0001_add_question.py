# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('total_response_count', models.IntegerField()),
                ('topic', models.CharField(max_length=20)),
                ('sequence_num', models.IntegerField()),
                ('multiple_valid_choices', models.BooleanField(default=False)),
            ],
        ),
    ]
