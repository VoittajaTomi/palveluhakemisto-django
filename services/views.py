# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import District, Service, ContactInfo
from .forms import AnonymousServiceForm, ContactInfoForm

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import json

from .serializers import ServiceSerializer, DistrictSerializer

from django.forms import inlineformset_factory



@csrf_exempt
def rest_all_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def rest_all_districts(request):
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return JsonResponse(serializer.data, safe=False)


def service_to_html(service):
    return {'balloonContentHeader': '<p>%s</p>' % service.description,
            'balloonContentBody': 'Address: %s<br>Phone: %s<br>Url<a href="%s">www</a>' % (service.contact_info.address, service.contact_info.phone, service.contact_info.url,),
            'balloonContentFooter': '<p>Helsingin kaupunginosayhdistykset Ry 2017</p>'
            }


def yandex_maps_json_feed_for_district(request, district_id):
    result = {'type' : 'FeatureCollection', 'features': []}
    feature_list = []
    district = District.objects.get(pk=district_id)
    for s in district.services.all():
        feature_list.append(
            {'type': 'Feature',
             'id': s.pk,
             'geometry': {'type': 'Point',
                          'coordinates': [s.gps_lat, s.gps_lon]},
             'properties': service_to_html(s)
             }
        )

    result['features'] = feature_list


    return HttpResponse(json.dumps(result),content_type="text/json")



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

    return render(request, 'services/view_district.html', {'district': district, 'services': district.services.all()})

def view_service(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        raise Http404('Service does not exist')

    return render(request,'services/view_service.html', {'service' : service})

def add_service(request):

    if request.method == 'POST':
        form = AnonymousServiceForm(request.POST)
        contactinfoform = ContactInfoForm(request.POST)
        if form.is_valid() and contactinfoform.is_valid():
            #import ipdb;ipdb.set_trace()
            form_desc = form.cleaned_data['description']
            form_district = form.cleaned_data['district']
            #form_address = form.cleaned_data['address']
            form_lat = form.cleaned_data['gps_lat']
            form_lon = form.cleaned_data['gps_lon']
            form_tags = form.cleaned_data['tags']
            form_address = contactinfoform.cleaned_data['address']
            form_phone = contactinfoform.cleaned_data['phone']
            form_zip = contactinfoform.cleaned_data['zip']
            form_url = contactinfoform.cleaned_data['url']
            contactinfo = ContactInfo.objects.create(address=form_address, zip=form_zip, url=form_url, phone=form_phone)
            service = Service.objects.create(description=form_desc, district=form_district, gps_lat=form_lat, gps_lon=form_lon, contact_info=contactinfo)
            map(service.tags.add, form_tags)
            service.save()

            return HttpResponseRedirect('/services')
    else:
        return render(request,'services/add_service.html', {'myform': AnonymousServiceForm, 'contactform': ContactInfoForm})
