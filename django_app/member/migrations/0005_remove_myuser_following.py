# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20170213_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='following',
        ),
    ]
