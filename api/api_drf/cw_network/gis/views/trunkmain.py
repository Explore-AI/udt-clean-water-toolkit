from cwa_geod.assets.models.trunk_main import TrunkMain
from rest_framework import permissions, viewsets 
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response 
from rest_framework.renderers import JSONRenderer 

# class TrunkMainViewSet(viewsets.ModelViewSet):
#     queryset = TrunkMain.objects.first(10)
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = TrunkMain

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@renderer_classes([JSONRenderer])
def get_all_trunkmain_data(request): 
    queryset = TrunkMain.objects.first(10)
    content = {'tm_data': queryset}
    return Response(content)
    