from cwageolachemy.config.db_config import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime 
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Utility(Base): 
    __tablename__="utilities_utility"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    modified_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    