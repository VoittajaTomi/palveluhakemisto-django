# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Service, District



class AnonymousServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('description', 'district', 'contact_info', 'gps_lat', 'gps_lon', 'tags')
        widgets = {
            'gps_lat': forms.NumberInput(attrs={'class':'kakka'}),
            'gps_lon': forms.NumberInput(attrs={'class': 'kakka'}),
        }


