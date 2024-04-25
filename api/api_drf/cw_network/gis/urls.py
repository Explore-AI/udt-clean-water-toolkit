# add gis urls here 
from django.urls import path 
from views import trunkmain 

urlpatterns = [
    path('trunkmain/', trunkmain, name='trunkmain'),
]