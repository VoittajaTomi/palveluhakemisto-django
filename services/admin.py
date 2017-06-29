# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import District, Service

# Register your models here.

admin.site.register(District)
admin.site.register(Service)
