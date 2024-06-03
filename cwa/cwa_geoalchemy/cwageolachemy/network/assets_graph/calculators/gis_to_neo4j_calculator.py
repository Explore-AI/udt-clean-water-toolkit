from ..models import NetworkNode

class GisToNeo4jCalculator: 
    
    def __init__(self): 
        pass 
    
    def read_point_node_data(self): 
        
        all_point_nodes = NetworkNode.nodes.all()
        count = 0 
        for node in all_point_nodes: 
            if count < 10: 
                print(node)
                count += 1
            else: 
                break 
