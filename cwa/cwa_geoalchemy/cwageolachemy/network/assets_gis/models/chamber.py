from ...assets_utilities.models.dma import DMA
from cwageolachemy.config.db_config import Base
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between chambers and the dmas
chamber_dmas = Table(
    "assets_chamber_dmas",
    Base.metadata,
    Column("chamber_id", Integer, ForeignKey("assets_chamber.id"), primary_key=True),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class Chamber(BasePointAsset):
    __tablename__ = "assets_chamber"
    dmas: Mapped[List[DMA]] = relationship(secondary=chamber_dmas)
    
    class AssetMeta: 
        asset_name = "chamber"
