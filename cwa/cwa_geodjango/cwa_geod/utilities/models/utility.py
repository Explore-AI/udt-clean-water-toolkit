from django.db import models
from cwa_geod.config.settings import UTILITIES


class Utility(models.Model):
    name = models.CharField(max_length=255, choices=UTILITIES, null=False, blank=False)

    def __str__(self):
        return self.name
