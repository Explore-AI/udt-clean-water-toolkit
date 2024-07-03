from rest_framework import serializers
from cwageodjango.assets.models.trunk_main import TrunkMain
from config.serializers import BaseGeoJsonSerializer


class TrunkMainSerializer(serializers.ModelSerializer):

    #    coords = serializers.SerializerMethodField()

    class Meta:
        model = TrunkMain
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ("id",)

    # def get_coords(self, obj):
    #     return {"x": obj.geometry.coords[0], "y": obj.geometry.coords[1]}


class TrunkMainGeoJsonSerializer(BaseGeoJsonSerializer):

    class Meta:
        model = TrunkMain
        fields = ["geojson"]
