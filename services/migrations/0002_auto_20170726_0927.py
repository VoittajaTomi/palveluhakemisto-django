# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-26 09:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='zip',
            field=models.CharField(max_length=5),
        ),
    ]