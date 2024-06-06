from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from cwageolachemy.config.db_config import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between consumptionmeters and the dmas
consumptionmeter_dmas = Table(
    "assets_consumptionmeter_dmas",
    Base.metadata,
    Column(
        "consumptionmeter_id",
        Integer,
        ForeignKey("assets_consumptionmeter.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class ConsumptionMeter(BasePointAsset):
    __tablename__ = "assets_consumptionmeter"
    dmas: Mapped[List[DMA]] = relationship(secondary=consumptionmeter_dmas)
    
    class AssetMeta: 
        asset_name = "consumption_meter"
