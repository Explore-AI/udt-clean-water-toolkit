from neo4j import GraphDatabase
from django.conf import settings

class Neo4jDriver: 
    _instance = None 
    
    @classmethod
    def instance(cls): 
        if cls._instance is None: 
            db_settings = settings.GRAPH_DATABASES['default']
            uri = f"bolt://{db_settings['HOST']}:{db_settings['PORT']}"
            cls._instance = GraphDatabase.driver(uri, auth=(db_settings['USER'], db_settings['PASSWORD']))
        return cls._instance 
    
    @classmethod
    def close(cls): 
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None