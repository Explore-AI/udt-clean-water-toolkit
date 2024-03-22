from ..db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime 
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

class Utility(Base): 
    __tablename__="utilities_utility"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    modified_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)