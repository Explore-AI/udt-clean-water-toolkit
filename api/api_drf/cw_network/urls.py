from django.urls import path, include


urlpatterns = [
    path('gis/', include('cw_network.gis.urls'))
]