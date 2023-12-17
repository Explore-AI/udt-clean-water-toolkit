from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from config.base_model import Base


class User(Base):
    first_name: Mapped[str] = mapped_column(String(254), nullable=False)
    last_name: Mapped[str] = mapped_column(String(254), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    def __repr__(self) -> str:
        return f"User(email={self.email!r})"
