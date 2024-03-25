from domain.config.config_manager import Settings as AppSettings
from domain.models.postgis_db import get_db
from sqlalchemy.orm import Session


def cleanwater_to_neo4j():
    pass

def main(): 
    settings = AppSettings()
    
if __name__ == "__main__":
    print("Our CWA Geoalchemy application!!")
    main()