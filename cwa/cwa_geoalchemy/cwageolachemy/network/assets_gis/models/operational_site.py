from ....core.db.gis_db import Base
from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between operationalsites and the dmas
operationalsite_dmas = Table(
    "assets_operationalsite_dmas",
    Base.metadata,
    Column(
        "operationalsite_id",
        Integer,
        ForeignKey("assets_operationalsite.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class OperationalSite(BasePointAsset):
    __tablename__ = "assets_operationalsite"
    dmas: Mapped[List[DMA]] = relationship(secondary=operationalsite_dmas)
