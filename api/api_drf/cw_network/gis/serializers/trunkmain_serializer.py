from rest_framework import serializers
from cwa_geod.assets.models.trunk_main import TrunkMain

class TrunkMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrunkMain
        fields = ['gid', 'geometry', 'dmas', 'modified_at', 'created_at']
        read_only_fields = ('id',)