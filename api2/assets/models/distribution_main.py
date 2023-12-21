from django.contrib.gis.db import models

# from core.models.dma import DMA  # unsure


class DistributionMain(models.Model):
    gisid = models.IntegerField(null=False, blank=False)
    shape_length = models.FloatField(null=False, blank=False)
    geometry = models.MultiLineStringField()  # unsure
    #    dma = models.ForeignKey(utilities.DMA, on_delete=models.CASCADE)  # unsure

    def __str__(self):
        return self.gisid
