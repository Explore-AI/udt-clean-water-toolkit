from ....core.db.postgis_db import Base
from ....utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between hydrants and the dmas
hydrant_dmas = Table(
    "assets_hydrant_dmas",
    Base.metadata,
    Column("hydrant_id", Integer, ForeignKey("assets_hydrant.id"), primary_key=True),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class Hydrant(BasePointAsset):
    __tablename__ = "assets_hydrant"
    dmas: Mapped[List[DMA]] = relationship(secondary=hydrant_dmas)
