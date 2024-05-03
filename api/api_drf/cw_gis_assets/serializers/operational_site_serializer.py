from cwageodjango.assets.models import OperationalSite
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer

class OperationalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalSite
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]

class OperationalSiteGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = OperationalSite
        fields = ["geojson"]