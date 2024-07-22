from rest_framework import serializers
from cwageodjango.assets.models.pipe_main import PipeMain
from config.serializers import BaseGeoJsonSerializer


class PipeMainSerializer(serializers.ModelSerializer):

    #    coords = serializers.SerializerMethodField()

    class Meta:
        model = PipeMain
        fields = ["tag", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ("id",)

    # def get_coords(self, obj):
    #     return {"x": obj.geometry.coords[0], "y": obj.geometry.coords[1]}


class PipeMainGeoJsonSerializer(BaseGeoJsonSerializer):

    class Meta:
        model = PipeMain
        fields = ["geojson"]
