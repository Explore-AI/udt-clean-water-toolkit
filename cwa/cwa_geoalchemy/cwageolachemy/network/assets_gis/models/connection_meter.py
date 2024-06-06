from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from cwageolachemy.config.db_config import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between connectionmeters and the dmas
connectionmeter_dmas = Table(
    "assets_connectionmeter_dmas",
    Base.metadata,
    Column(
        "connectionmeter_id",
        Integer,
        ForeignKey("assets_connectionmeter.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class ConnectionMeter(BasePointAsset):
    __tablename__ = "assets_connectionmeter"
    dmas: Mapped[List[DMA]] = relationship(secondary=connectionmeter_dmas)
    
    class AssetMeta: 
        asset_name = "connection_meter"
