from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """This is an abstract base class. It should not be
    instantiated directly. It should only be used as an inherited
    class.
    """

    #__abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
