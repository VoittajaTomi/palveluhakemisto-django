# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager


#from .forms import AnonymousServiceForm

# Create your models here.
#import floppyforms.__future__ as forms




class District(models.Model):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50)
    ctr_lat = models.FloatField(default=60.192059)
    ctr_lon = models.FloatField(default=24.945831)
    map_zoom = models.PositiveIntegerField(default=12)
    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=21, default='', blank=True)
    zip = models.CharField(max_length=5, blank=True)
    url = models.CharField(max_length=3000, default='',blank=True)

class Service(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='services')
    description = models.CharField(max_length=100)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    tags = TaggableManager()
    contact_info = models.OneToOneField(ContactInfo)
    is_accessible = models.BooleanField(default=True)

    def taglist(self):
        return ','.join(list(t.name for t in self.tags.all()))

    def __str__(self):
        return self.description


