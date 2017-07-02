# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.template import loader
# Create your views here.
from .models import District, Service, AnonymousServiceForm


def index(request):

    districts = District.objects.all()
    services = Service.objects.all()
    context = {'districts': districts, 'services': services}

    return render(request, 'services/index.html', context)

def view_service(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        raise Http404('Service does not exist')

    return render(request,'services/view_service.html', {'service' : service})

def add_service(request):

    return render(request,'services/add_service.html', {'myform': AnonymousServiceForm})
