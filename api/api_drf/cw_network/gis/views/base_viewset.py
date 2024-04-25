# here is data 
from rest_framework import viewsets
from ..pagination import StandardResultsSetPagination

class BaseViewSet(viewsets.ReadOnlyModelViewSet): 
    pagination_class = StandardResultsSetPagination
    