from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from cwageolachemy.config.db_config import Base
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between pressurecontrolvalves and the dmas
pressurecontrolvalve_dmas = Table(
    "assets_pressurecontrolvalve_dmas",
    Base.metadata,
    Column(
        "pressurecontrolvalve_id",
        Integer,
        ForeignKey("assets_pressurecontrolvalve.id"),
        primary_key=True,
    ),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class PressureControlValve(BasePointAsset):
    __tablename__ = "assets_pressurecontrolvalve"
    dmas: Mapped[List[DMA]] = relationship(secondary=pressurecontrolvalve_dmas)
    
    class AssetMeta: 
        asset_name = "pressure_control_valve"
