# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import floppyforms.__future__ as forms
#from django import forms

"""

    __tablename__ = 'services'
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), primary_key=True)
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district = db.relationship('District', backref='services')
    desc = db.Column(db.String(50))
    address = db.Column(db.String(50))
    gps_lat = db.Column(db.Float)
    gps_lon = db.Column(db.Float)


    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(50))

    def __str__(self):
        return self.desc


"""


class District(models.Model):
    description = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50)
    ctr_lat = models.FloatField(default=60.192059)
    ctr_lon = models.FloatField(default=24.945831)

    def __str__(self):
        return self.name

class Service(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()

    def __str__(self):
        return self.description



class AnonymousServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('description', 'district', 'address', 'gps_lat', 'gps_lon')
        widgets = {
            'gps_lat': forms.NumberInput(attrs={'class':'kakka'}),
            'gps_lon': forms.NumberInput(attrs={'class': 'kakka'}),
        }

