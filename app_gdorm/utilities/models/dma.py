from django.db import models


class DMA(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    network_repr = models.JSONField(null=True)

    def __str__(self):
        return self.code

    class Meta:
        # https://stackoverflow.com/questions/16800375/how-can-i-set-two-primary-key-fields-for-my-models-in-django
        # This is not neccesary. Just trying something out. It can be removed safely.
        constraints = [models.UniqueConstraint(fields=["id", "code"], name="id_code")]
