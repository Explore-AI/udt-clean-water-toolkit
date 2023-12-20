from django.contrib.gis.db  import Model, IntegerField, FloatField
# from core.models.dma import DMA

class Hydrant(Model):

    def __str__(self):
        return self.name