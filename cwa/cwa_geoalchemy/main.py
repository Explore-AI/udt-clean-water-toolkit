from cwageolachemy.config.config_manager import Settings as AppSettings
from cwa.cwa_geoalchemy.cwageolachemy.core.db.gis_db import get_db, session_local
from sqlalchemy.orm import Session
from cwageolachemy.network.assets_utilities.models.dma import DMA
from cwageolachemy.network.assets_utilities.models.utility import Utility
from cwageolachemy.network.assets_gis.models import * 
from sqlalchemy import select


def cleanwater_to_neo4j():
    pass

def main(): 
    settings = AppSettings()
    session = session_local()
        
if __name__ == "__main__":
    print("Our CWA Geoalchemy application!!")
    main()