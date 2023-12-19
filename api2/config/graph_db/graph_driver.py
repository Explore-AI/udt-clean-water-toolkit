from neo4j import GraphDatabase
from config.settings import GRAPH_DATABASES


class GraphDatabaseDriver:
    def __init__(self, uri, user, password):
        self.driver = None

    def __enter__(self):
        neo4j_db = GRAPH_DATABASES.get("default")

        # add exception handling
        uri = f"{neo4j_db.get('HOST')}:{neo4j_db.get('PORT')}"
        self.driver = GraphDatabase.driver(
            uri, auth=(neo4j_db.get("USER"), neo4j_db.get("PASSWORD"))
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
