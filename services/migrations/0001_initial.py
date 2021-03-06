# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 11:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default='', max_length=100)),
                ('phone', models.CharField(blank=True, default='', max_length=21)),
                ('zip', models.CharField(blank=True, max_length=5)),
                ('url', models.CharField(blank=True, default='', max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(max_length=50)),
                ('ctr_lat', models.FloatField(default=60.192059)),
                ('ctr_lon', models.FloatField(default=24.945831)),
                ('map_zoom', models.PositiveIntegerField(default=12)),
                ('admin', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('gps_lat', models.FloatField()),
                ('gps_lon', models.FloatField()),
                ('is_accessible', models.BooleanField(default=True)),
                ('contact_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.ContactInfo')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.District')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
