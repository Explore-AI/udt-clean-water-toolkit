from django.db import models


class DMA(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    network_repr = models.JSONField(null=True)

    def __str__(self):
        return self.code

    class Meta:
        constraints = [models.UniqueConstraint(fields=["id", "code"], name="id_code")]
