from ...core.db.postgis_db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime 
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Utility(Base): 
    __tablename__="utilities_utility"
    
    # id = Column(Integer, primary_key=True)
    # name = Column(String(255), nullable=False, unique=True)
    # modified_at = Column(DateTime, nullable=False)
    # created_at = Column(DateTime, nullable=False)
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    