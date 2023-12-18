from django.db.models import Model, IntegerField, FloatField

# from core.models.dma import Dma


class Logger(Model):
    gisid = IntegerField(null=False, blank=False)
    shape_y = FloatField(max_length=50, null=False, blank=False)
    shape_x = FloatField(max_length=50, null=False, blank=False)
    # geometry = CharField(max_length=50, null=False, blank=False) # this should be a geospation field
    # dma = ForeignKey(Dma, on_delete=CASCADE, related_name="dma_loggers")
