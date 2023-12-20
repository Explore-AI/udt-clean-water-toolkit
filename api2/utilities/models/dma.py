from django.db.models import Model, CharField, JSONField

class DMA(Model):
    code=CharField(max_length=50)       #need to check max_length
    network_repr=JSONField()

    def __str__(self):
        return self.name

