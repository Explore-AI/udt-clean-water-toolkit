from django.contrib.gis.db.models  import Model, IntegerField, FloatField, MultiLineStringField, ForeignKey
# from core.models.dma import DMA    #unsure

class TrunkMain(Model):
    GISID = IntegerField(null=False, blank=False)
    SHAPE_Length = FloatField(max_length=50, null=False, blank=False)
    geometry = MultiLineStringField()                      #unsure
    DMACODE = ForeignKey(utilities.DMA,on_delete=CASCADE)  #unsure

    def __str__(self):
        return self.name