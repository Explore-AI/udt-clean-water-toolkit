from cwageolachemy.config.config_manager import Settings as AppSettings
from cwageolachemy.core.db.postgis_db import get_db, session_local
from sqlalchemy.orm import Session
from cwageolachemy.utilities.models.dma import DMA
from cwageolachemy.utilities.models.utility import Utility
from sqlalchemy import select


def cleanwater_to_neo4j():
    pass

def main(): 
    settings = AppSettings()
    
    # with get_db() as session:
    session = session_local()
    # load data from the DMA table 
    
    # get all records from the utility table 
    utility_query = select(Utility).where(Utility.name == "THAMES WATER")
    results = session.execute(utility_query)
    util_results = results.all()
    
    
    
if __name__ == "__main__":
    print("Our CWA Geoalchemy application!!")
    main()