from django.db import models


class DMA(models.Model):
    code = models.CharField(max_length=50)
    network_repr = models.JSONField()

    def __str__(self):
        return self.code
