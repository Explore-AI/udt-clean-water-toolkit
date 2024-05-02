from cwageodjango.assets.models import DistributionMain
from rest_framework import serializers


class DistributionMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionMain
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
