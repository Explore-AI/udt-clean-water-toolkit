from cwageodjango.assets.models import DistributionMain
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer


class DistributionMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionMain
        fields = ["tag", "geometry", "dmas", "modified_at", "created_at"]


class DistributionMainGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = DistributionMain
        fields = ["geojson"]
