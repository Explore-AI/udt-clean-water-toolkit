from sqids import Sqids
from wntr import network

class Neo4j2Wntr:
    """
    Class for converting data from Neo4j graph database to Water Network Toolkit (WNTR) format.

    """
    def __init__(self):
        self.wn = network.WaterNetworkModel()
        self.sqid_alphabet = '9ItmZiAJ4OFa6MPCv5sDEpyGb2UQfWhTNlrgcnB0odz8KqVkRX3L1wYHeSu7jx'
        self.sqids = Sqids(alphabet=self.sqid_alphabet)

    def generate_unique_id(self, input_string):
        """
        Generates a unique ID for the given input string.

        Parameters:
            input_string (str): Input string for which the unique ID is generated.

        Returns:
            unique_id (str): Unique ID generated using SQID encoding.

        """
        unique_id = self.sqids.encode([input_string])
        return str(unique_id)

    def add_node(self, id, x, y):
        """
        Adds a node to the water network model.

        Parameters:
            id (str): ID of the node.
            x (float): X-coordinate of the node.
            y (float): Y-coordinate of the node.

        Returns:
            node_id (str): SQIDS ID of the added node.

        """
        node_id = self.generate_unique_id(id)
        self.wn.add_junction(node_id, coordinates=(x, y))
        return node_id
    
    def add_pipe(self, edge_id, start_node_id, end_node_id):
        """
        Adds a pipe to the water network model.

        Parameters:
            edge_id (str): ID of the edge (pipe).
            start_node_id (str): ID of the start node.
            end_node_id (str): ID of the end node.

        Returns:
            pipe_id (str): SQIDS ID of the added pipe.

        """
        pipe_id = self.generate_unique_id(edge_id)
        self.wn.add_pipe(pipe_id, start_node_id, end_node_id)
        return pipe_id
        
    def process_batch(self, batch_result):
        """
        Processes a batch of results from Neo4j query and adds corresponding nodes and pipes to the water network model.

        Parameters:
            batch_result (list): List of results from Neo4j query.

        """
        for i in batch_result:
            start = i[1]._start_node
            x, y = start['x_coord'], start['y_coord']
            start_id = start._id
            start_node_id = self.add_node(start_id, x, y)

            end = i[1]._end_node
            x, y = end['x_coord'], end['y_coord']
            end_id = end._id
            end_node_id = self.add_node(end_id, x, y)

            edge_id = i[1]._id
            pipe_id = self.add_pipe(edge_id, start_node_id, end_node_id)