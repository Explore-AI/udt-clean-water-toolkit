from ....core.constants import DEFAULT_SRID
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry
from datetime import datetime
from cwageolachemy.config.db_config import Base


class BaseAsset(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gid: Mapped[int] = mapped_column(Integer)
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    


class BaseMainsAsset(BaseAsset):
    __abstract__ = True
    geometry: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=DEFAULT_SRID)
    )
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: id: {self.id}, gid: {self.gid}, geometry: {self.geometry}>"


class BasePointAsset(BaseAsset):
    __abstract__ = True
    geometry: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POINT", srid=DEFAULT_SRID)
    )
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: id: {self.id}, gid: {self.gid}, geometry: {self.geometry}>"
