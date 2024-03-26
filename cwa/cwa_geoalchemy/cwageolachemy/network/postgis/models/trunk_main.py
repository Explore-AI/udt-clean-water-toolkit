from typing import List
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, relationship
from ....core.db.postgis_db import Base
from ....utilities.models.dma import DMA
from .base_gis_asset import BaseMultiStringAsset

trunkmain_dmas = Table(
    "assets_trunkmain_dmas",
    Base.metadata,
    Column("trunkmain_id", Integer, ForeignKey("assets_trunkmain.id")),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id")),
)


class TrunkMain(BaseMultiStringAsset):
    __tablename__ = "assets_trunkmain"
    dmas: Mapped[List[DMA]] = relationship(secondary=trunkmain_dmas)
