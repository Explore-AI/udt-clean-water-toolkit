from cwa_geod.config.settings import sqids
from wntr import network

class Neo4j2Wntr:
    def __init__(self):
        self.wn = network.WaterNetworkModel()
        self.values_to_drop = ['PointAsset', 'PointNode']
    
    def generate_unique_id(self, input_string):
        # Encode the input string using SQID
        unique_id = sqids.encode([input_string])
        return str(unique_id)

    def add_node(self, element_id, x, y):
        node_id = self.generate_unique_id(element_id)
        self.wn.add_junction(node_id, coordinates=(x, y))
        return node_id
    
    def add_pipe(self, edge_elementid, start_node_id, end_node_id):
        pipe_id = self.generate_unique_id(edge_elementid)
        self.wn.add_pipe(pipe_id, start_node_id, end_node_id)
        return pipe_id
        
    def _process_batch(self, batch_result):
        for i in batch_result:
            start = i[1]._start_node
            x, y = start['x_coord'], start['y_coord']
            start_node_elementid = start._id
            start_node_id = self.add_node(start_node_elementid, x, y)

            end = i[1]._end_node
            x, y = end['x_coord'], end['y_coord']
            end_node_elementid = end._id
            end_node_id = self.add_node(end_node_elementid, x, y)

            edge_elementid = i[1]._id
            pipe_id = self.add_pipe(edge_elementid, start_node_id, end_node_id)