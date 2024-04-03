from ....core.db.gis_db import Base
from ....core.constants import DEFAULT_SRID
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from geoalchemy2 import Geometry
from datetime import datetime


class BaseAsset(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gid: Mapped[int] = mapped_column(Integer)
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} - {self.gid}>"


class BasePointAsset(BaseAsset):
    __abstract__ = True
    geometry: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POINT", srid=DEFAULT_SRID)
    )


class BaseMainsAsset(BaseAsset):
    __abstract__ = True
    geometry: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=DEFAULT_SRID)
    )
