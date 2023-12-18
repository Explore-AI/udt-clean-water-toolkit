from django.db.models import Model, CharField, DateTimeField

# from core.models.dma import Dma


class Logger(Model):
    gisid = CharField(max_length=50, null=False, blank=False)
    date_created = DateTimeField(null=False, blank=False)
    gps_x = CharField(max_length=50, null=False, blank=False)
    gps_y = CharField(max_length=50, null=False, blank=False)
    gps_z = CharField(max_length=50, null=False, blank=False)
    shape_y = CharField(max_length=50, null=False, blank=False)
    shape_x = CharField(max_length=50, null=False, blank=False)
    geometry = CharField(max_length=50, null=False, blank=False)
    # dma = ForeignKey(Dma, on_delete=CASCADE, related_name="dma_loggers")
