from ....core.db.postgis_db import Base
from ....utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between pressurefittings and the dmas
pressurefitting_dmas = Table(
    "assets_pressurefitting_dmas",
    Base.metadata,
    Column(
        "pressurefitting_id",
        Integer,
        ForeignKey("assets_pressurefitting.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class PressureFitting(BasePointAsset):
    __tablename__ = "assets_pressurefitting"
    dmas: Mapped[List[DMA]] = relationship(secondary=pressurefitting_dmas)
