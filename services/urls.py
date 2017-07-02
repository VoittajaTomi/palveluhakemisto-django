from django.conf.urls import url

from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^(?P<service_id>[0-9]+)/$', views.view_service, name='view_service'),
               url(r'^add', views.add_service, name='add_service')]