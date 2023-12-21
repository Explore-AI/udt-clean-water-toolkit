from django.contrib.gis.db.models import (
    Model,
    IntegerField,
    FloatField,
    PointField,
    ForeignKey,
)

# from core.models.dma import DMA   #unsure


class Hydrant(Model):
    GISID = IntegerField(null=False, blank=False)
    SHAPEX = FloatField(null=False, blank=False)
    SHAPEY = FloatField(null=False, blank=False)
    geometry = PointField()  # unsure
    #    DMACODE = ForeignKey(utilities.DMA,on_delete=CASCADE)  #unsure

    def __str__(self):
        return self.name
