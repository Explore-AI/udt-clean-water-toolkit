from cwageolachemy.config.config_manager import Settings as AppSettings
from cwageolachemy.core.db.postgis_db import get_db, session_local
from sqlalchemy.orm import Session
from cwageolachemy.utilities.models.dma import DMA
from cwageolachemy.utilities.models.utility import Utility
from cwageolachemy.network.postgis.models import * 
from sqlalchemy import select


def cleanwater_to_neo4j():
    pass

def main(): 
    settings = AppSettings()
    session = session_local()
        
if __name__ == "__main__":
    print("Our CWA Geoalchemy application!!")
    main()