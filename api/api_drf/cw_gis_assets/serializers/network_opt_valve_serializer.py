from cwageodjango.assets.models import NetworkOptValve
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer


class NetworkOptValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOptValve
        fields = ["tag", "geometry", "dmas", "modified_at", "created_at"]


class NetworkOptValveGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = NetworkOptValve
        fields = ["geojson"]
