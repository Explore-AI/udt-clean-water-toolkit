import argparse 
from cwageolachemy.network.assets_graph.controllers.gis_to_neo4j_controller import GisToNeo4jController

class Analysis(): 
    def __init__(self): 
        pass 
    
    def run(self): 
        gis_to_neo4j_controller = GisToNeo4jController()
        gis_to_neo4j_controller.create_network()
    

