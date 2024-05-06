from rest_framework import serializers


class BaseGeoJsonSerializer(serializers.ModelSerializer):
    geojson = serializers.SerializerMethodField()

    class Meta:
        fields = ["geojson"]
        abstract = True

    def get_geojson(self, obj):
        return obj
