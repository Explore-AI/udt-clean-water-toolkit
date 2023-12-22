from django.contrib.gis.db import models
from utilities.models.dma import DMA 


class Logger(models.Model):
    gisid = models.IntegerField(null=False, blank=False)
    shape_x = models.FloatField(null=False, blank=False)
    shape_y = models.FloatField(null=False, blank=False)
    geometry = models.PointField()  
    dma_1 = models.ForeignKey(DMA,on_delete=models.CASCADE,related_name="logger_dma_1")

    def __str__(self):
        return self.gisid
