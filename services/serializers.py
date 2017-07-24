from rest_framework import serializers
from .models import Service, District
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class ServiceSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Service
        fields = ('__all__')

class DistrictSerializer(serializers.ModelSerializer):

    services = serializers.StringRelatedField(many=True)

    class Meta:
        model = District
        fields = ('__all__') #adasd