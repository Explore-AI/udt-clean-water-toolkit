# db session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cwageolachemy.config.config_manager import Settings as AppSettings 

app_settings = AppSettings()
HOST = app_settings.POSTGIS_DEFAULT_DB_HOST
NAME = app_settings.POSTGIS_DB_NAME
USER = app_settings.POSTGIS_DB_USER
PASSWORD = app_settings.POSTGIS_DEFAULT_DB_PASSWORD


engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}")

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

