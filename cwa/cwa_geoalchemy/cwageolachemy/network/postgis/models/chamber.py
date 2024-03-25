from ....core.db.postgis_db import Base
from ....utilities.models.dma import DMA
from sqlalchemy import Column, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

# junction table between chambers and the dmas
chamber_dmas = Table(
    "assets_chamber_dmas",   
    Base.metadata,  
    Column("chamber_id", Integer, ForeignKey("assets_chamber.id")),
    Column("dma_id", Integer, ForeignKey("utilities_dma.code")) 
)


class Chamber(Base): 
    __tablename__ = 'assets_chamber'
    
    id = Column(Integer, primary_key=True)
    gid = Column(Integer, nullable=False)
    geometry = Column(Geometry(geometry_type='POINT', srid=27700), nullable=False)
    modified_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # doing more research on defining the many to many relationship
    dmas = relationship('DMA', secondary=chamber_dmas, back_populates="utilities_dma")

