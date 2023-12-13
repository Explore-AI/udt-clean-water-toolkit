from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from fastapi import Depends
from config.settings import DB_URL

SQLALCHEMY_DATABASE_URL = DB_URL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def db_session(depends: bool = True):
#     if depends:
#         return Depends(get_db)
#     return get_db


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#using-context-managers-in-dependencies-with-yield
class DBSession:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


# There appears to be a bug with the usage of next(). See link above.
def db_session():
    with DBSession() as db:
        yield db
