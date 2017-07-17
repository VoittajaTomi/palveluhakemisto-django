from rest_framework import serializers
from .models import Service, District

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('__all__')

class DistrictSerializer(serializers.ModelSerializer):

    services = serializers.StringRelatedField(many=True)

    class Meta:
        model = District
        fields = ('__all__') #adasd