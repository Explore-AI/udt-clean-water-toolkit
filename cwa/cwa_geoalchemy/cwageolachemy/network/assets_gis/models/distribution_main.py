
from ...assets_utilities.models.dma import DMA
from cwageolachemy.config.db_config import Base
from .base_gis_asset import BaseMainsAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List


distributionmain_dmas = Table(
    "assets_distributionmain_dmas",
    Base.metadata,
    Column("distributionmain_id", Integer, ForeignKey("assets_distributionmain.id")),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id")),
)


class DistributionMain(BaseMainsAsset):
    __tablename__ = "assets_distributionmain" 
    dmas: Mapped[List[DMA]] = relationship(secondary=distributionmain_dmas)
    
    class AssetMeta: 
        asset_name = "distribution_main"
