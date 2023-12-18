from django.db.models import Model, CharField


class Dma(Model):
    dma_code = CharField(max_length=50, null=False, blank=False)
    # networkx = JsonField()
