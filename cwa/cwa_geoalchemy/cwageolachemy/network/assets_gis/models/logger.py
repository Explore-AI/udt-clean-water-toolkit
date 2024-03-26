from ....core.db.gis_db import Base
from ...assets_utilities.models.dma import DMA
from .base_gis_asset import BasePointAsset
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from typing import List

# join table between loggers and the dmas
logger_dmas = Table(
    "assets_logger_dmas",
    Base.metadata,
    Column("logger_id", Integer, ForeignKey("assets_logger.id"), primary_key=True),
    Column("dma_id", Integer, ForeignKey("utilities_dma.id"), primary_key=True),
)


class Logger(BasePointAsset):
    __tablename__ = "assets_logger"
    dmas: Mapped[List[DMA]] = relationship(secondary=logger_dmas)
