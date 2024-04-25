from django.urls import path, include


url_patterns = [
    path('gis/', include('network.gis.urls'))
]