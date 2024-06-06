from typing import List
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, relationship
from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BaseMainsAsset
from cwageolachemy.config.db_config import Base

connectionmain_dmas = Table(
    "assets_connectionmain_dmas",
    Base.metadata,
    Column("connectionmain_id", Integer, ForeignKey("assets_tconnectionmain.id")),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id")),
)


class ConnectionMain(BaseMainsAsset):
    __tablename__ = "assets_connectionmain"
    dmas: Mapped[List[DMA]] = relationship(secondary=connectionmain_dmas)

    class AssetMeta: 
        asset_name = "connection_main"