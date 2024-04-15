from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from cwageolachemy.config.db_config import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between networkoptvalves and the dmas
networkoptvalve_dmas = Table(
    "assets_networkoptvalve_dmas",
    Base.metadata,
    Column(
        "networkoptvalve_id",
        Integer,
        ForeignKey("assets_networkoptvalve.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class NetworkOptValve(BasePointAsset):
    __tablename__ = "assets_networkoptvalve"
    dmas: Mapped[List[DMA]] = relationship(secondary=networkoptvalve_dmas)
    
    class AssetMeta: 
        asset_name = "network_opt_valve"
