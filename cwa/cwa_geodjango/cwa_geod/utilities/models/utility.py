from django.db import models
from cwa_geod.core.constants import UTILITIES


class Utility(models.Model):
    name = models.CharField(
        max_length=255, choices=UTILITIES, null=False, blank=False, index=True
    )
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name
