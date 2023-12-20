from neo4j import GraphDatabase
from config.settings import GRAPH_DATABASES


def init_graphdb(func):
    def wrapper():
        with _GraphDatabaseDriver():
            func()

    return wrapper


class _GraphDatabaseDriver:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        neo4j_db = GRAPH_DATABASES.get("default")

        # add exception handling
        uri = f"{neo4j_db.get('HOST')}:{neo4j_db.get('PORT')}"
        user = neo4j_db.get("USER")
        password = neo4j_db.get("PASSWORD")

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
