from django.contrib.gis.db import models
from utilities.models.dma import DMA

class TrunkMain(models.Model):
    gisid = models.IntegerField(null=False, blank=False)
    shape_length = models.FloatField(null=False, blank=False)
    geometry = models.MultiLineStringField() 
    dma = models.ForeignKey(DMA, on_delete=models.CASCADE,related_name="trunk_dma")  
    
    def __str__(self):
        return self.gisid