from cwageolachemy.config.config_manager import Settings as AppSettings
from cwageolachemy.core.db.gis_db import get_db, session_local
from cwageolachemy.core.analysis import Analysis


def main(): 
    analysis = Analysis()
    analysis.run()

        
if __name__ == "__main__":
    main()