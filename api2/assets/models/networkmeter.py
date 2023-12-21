from django.contrib.gis.db.models import Model, IntegerField, FloatField, PointField, ForeignKey
# from core.models.dma import DMA    #unsure

class NetworkMeter(Model):
    GISID = IntegerField(null=False, blank=False)
    SHAPEX = FloatField(max_length=50, null=False, blank=False)
    SHAPEY = FloatField(max_length=50, null=False, blank=False)
    geometry = PointField()    
    DMACODE1 = ForeignKey(utilities.DMA1,on_delete=CASCADE)  #can possibly be created
    DMACODE2 = ForeignKey(utilities.DMA2,on_delete=CASCADE)  #can possibly be created

    def __str__(self):
        return self.name