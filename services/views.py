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
            'balloonContentBody': 'Lorem ipsum dolor sit amet consectetur adipiscing elit fusce, aenean parturient senectus sociosqu consequat felis ligula, habitasse mollis class pretium penatibus vivamus ante. Non per primis nullam turpis duis tristique erat nam, parturient sagittis montes felis maecenas fermentum feugiat volutpat, vestibulum nulla nibh faucibus egestas euismod sollicitudin. Sollicitudin netus luctus tempor sociosqu auctor convallis tortor sociis, erat rutrum nascetur neque platea cursus gravida, eu ac dis natoque nisi mollis fusce. Ornare gravida arcu rutrum in tempor hac venenatis faucibus aenean, a morbi netus ad quam facilisis id aptent, ullamcorper euismod natoque fringilla auctor torquent nisl tellus. Arcu turpis habitasse natoque eros pretium cursus odio feugiat potenti scelerisque varius iaculis facilisis morbi fames orci, nascetur suscipit conubia montes velit phasellus sed faucibus consequat habitant a magna laoreet aptent. Ullamcorper ante lobortis vitae curabitur nulla suscipit inceptos in bibendum, aptent imperdiet cum mollis class nascetur nibh curae, at gravida purus risus sed vel sagittis non. Ultricies laoreet lectus orci turpis lobortis odio proin varius ultrices in mattis, a egestas scelerisque donec morbi sagittis himenaeos eget quis platea, sodales dapibus nullam aptent penatibus condimentum hac parturient fermentum fringilla.',
            'balloonContentFooter': '<p>Footer</p>'
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
            service = Service.objects.create(description=form_desc, district=form_district, gps_lat=form_lat, gps_lon=form_lon,)
            map(service.tags.add, form_tags)
            #for t in form_tags:
            #    service.tags.add(t)

            service.save()

            return HttpResponseRedirect('/services')
    else:
        return render(request,'services/add_service.html', {'myform': AnonymousServiceForm, 'contactform': ContactInfoForm})
