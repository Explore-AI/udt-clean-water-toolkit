from django.db.models import Model, CharField, JSONField

#from django.contrib.gis.db.models import Model
#from core.models.dma import Dma


class DMA(Model):
    code=CharField(max_length=50)       #need to check max_length
    network_repr=JSONField()

    #possibly a GeoDjango specific geometry field (MultiPolygonField)

    def __str__(self):
        return self.name

