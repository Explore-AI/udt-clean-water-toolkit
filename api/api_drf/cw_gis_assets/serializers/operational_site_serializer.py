from cwageodjango.assets.models import OperationalSite
from rest_framework import serializers


class OperationalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalSite
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
