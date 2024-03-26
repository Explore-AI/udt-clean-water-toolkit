from ...core.db.postgis_db import Base
from sqlalchemy import String, DateTime, JSON, Integer
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime


class DMA(Base):
    __tablename__ = "utilities_dma"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(255))
    network_repr: Mapped[Optional[dict]] = mapped_column(JSON)
    geometry: Mapped[Geometry] = mapped_column(Geometry(geometry_type="MULTIPOLYGON", srid=27700, spatial_index=True))
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
