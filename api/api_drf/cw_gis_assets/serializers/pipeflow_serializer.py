from rest_framework import serializers
from cwageodjango.assets.models import PipeMain
from cwageodjango.waterpipes.models import PipeFlow


class PipeMainSerializer(serializers.ModelSerializer):

    class Meta:
        model = PipeMain
        fields = ["tag", "dmas", "id"]


class PipeFlowSerializer(serializers.ModelSerializer):
    pipe_main = PipeMainSerializer()
    tag = serializers.CharField(source="pipe_main.tag", read_only=True)
    id = serializers.CharField(source="pipe_main.id", read_only=True)
    dmas = serializers.CharField(source="pipe_main.dmas", read_only=True)
    #    pipe_flow = serializers.SerializerMethodField()

    class Meta:
        model = PipeFlow
        fields = ["pipe_main", "flow_data", "id", "tag", "dmas"]

    # def get_pipe_flow(self, obj):
    #     import pdb

    #     pdb.set_trace()
    #     return obj
