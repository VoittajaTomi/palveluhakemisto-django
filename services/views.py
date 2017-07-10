# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
from .models import District, Service, AnonymousServiceForm


def index(request):

    districts = District.objects.all()
    services = Service.objects.all()
    context = {'districts': districts, 'services': services}

    return render(request, 'services/index.html', context)

def view_district(request, district_id):
    #return HttpResponse("Hello " + district_id)

    try:
        district = District.objects.get(pk=district_id)
    except District.DoesNotExist:
        raise Http404('District does not exist')

    return render(request, 'services/view_district.html', {'district': district})

def view_service(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        raise Http404('Service does not exist')

    return render(request,'services/view_service.html', {'service' : service})

def add_service(request):

    if request.method == 'POST':
        form = AnonymousServiceForm(request.POST)
        if form.is_valid():
            form_desc = form.cleaned_data['description']
            form_district = form.cleaned_data['district']
            form_address = form.cleaned_data['address']
            form_lat = form.cleaned_data['gps_lat']
            form_lon = form.cleaned_data['gps_lon']

            s = Service.objects.create(description=form_desc, district=form_district, address = form_address, gps_lat = form_lat, gps_lon = form_lon)

            return HttpResponseRedirect('/services')
    else:
        return render(request,'services/add_service.html', {'myform': AnonymousServiceForm})
