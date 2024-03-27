from ....core.db.gis_db import Base
from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between networkmeters and the dmas
networkmeter_dmas = Table(
    "assets_networkmeter_dmas",
    Base.metadata,
    Column(
        "networkmeter_id",
        Integer,
        ForeignKey("assets_networkmeter.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class NetworkMeter(BasePointAsset):
    __tablename__ = "assets_networkmeter"
    dmas: Mapped[List[DMA]] = relationship(secondary=networkmeter_dmas)
