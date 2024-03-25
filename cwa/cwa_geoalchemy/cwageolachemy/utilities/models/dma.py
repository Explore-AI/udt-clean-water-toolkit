from ...core.db.postgis_db import Base
from .utility import Utility
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime


class DMA(Base):
    
    __tablename__ = "utilities_dma"

    # code = Column(String, primary_key=True)
    # name = Column(String, nullable=False)
    # # utility_id = Column(Integer, ForeignKey("utility.id"), nullable=False)
    # # utility = relationship("Utility", back_populates="utility_dmas")
    # network_repr = Column(JSON, nullable=True)
    # geometry = Column(
    #     Geometry(geometry_type="MULTIPOLYGON", srid=27700, spatial_index=True),
    #     nullable=False,
    # )
    # modified_at = Column(DateTime, nullable=False)
    # created_at = Column(DateTime, nullable=False)
    
    code: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    network_repr: Optional[Mapped[dict]] = mapped_column(JSON, nullable=True)
    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type="MULTIPOLYGON", srid=27700, spatial_index=True))
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
