from django.contrib.gis.db import models
from utilities.models.dma import DMA


class Hydrant(models.Model):
    gisid = models.IntegerField(null=False, blank=False)
    shape_x = models.FloatField(null=False, blank=False)
    shape_y = models.FloatField(null=False, blank=False)
    geometry = models.PointField()
    dma = models.ForeignKey(DMA, on_delete=models.CASCADE, related_name="dma_hydrants")

    def __str__(self):
        return self.gisid
