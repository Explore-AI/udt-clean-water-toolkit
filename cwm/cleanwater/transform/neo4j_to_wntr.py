import wntr
from wntr import network
import pandas as pd
import numpy as np

class Neo4j2Wntr:
    """
    Convert a Neo4j graph to the Water Network Toolkit (WNTR) format.
    """
    def __init__(self, sqids):
        self.wn = network.WaterNetworkModel()
        self.sqids = sqids
        self.roughness_values = self.load_roughness_values('material_roughness.csv')

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

    @staticmethod
    def generate_random_value(min_value, max_value):
        """
        Generate a random value within the specified range.
        """
        return np.random.uniform(min_value, max_value)

    @staticmethod
    def load_roughness_values(csv_path):
        """
        Load roughness values from a CSV file into a dictionary.
        """
        try:
            df = pd.read_csv(csv_path)
            roughness_dict = pd.Series(df.roughness.values, index=df.material).to_dict()
            return roughness_dict
        except Exception as e:
            return {}

    @staticmethod
    def convert_coords(coords):
        """
        Helper function to convert coords_27700 to a tuple.
        """
        return tuple(coords)

    def add_node(self, id, coordinates, elevation, base_demand):
        """
        Adds a node to the water network model.

        Parameters:
            id (str): ID of the node.
            x (float): X-coordinate of the node.
            y (float): Y-coordinate of the node.
            elevation (float): Elevation of the node.
            base_demand (float): Base demand at the node.

        Returns:
            node_id (str): SQIDS ID of the added node.
        """
        node_id = self.generate_unique_id(id)
        self.wn.add_junction(node_id, elevation=elevation, base_demand=base_demand, coordinates=coordinates)
        return node_id

    def add_pipe(self, edge_id, start_node_id, end_node_id, diameter, length, roughness=100.0):
        """
        Adds a pipe to the water network model.

        Parameters:
            edge_id (str): ID of the edge (pipe).
            start_node_id (str): ID of the start node.
            end_node_id (str): ID of the end node.
            diameter (float): Diameter of the pipe.
            length (float): Length of the pipe.
            roughness (float): Roughness coefficient of the pipe.

        Returns:
            pipe_id (str): SQIDS ID of the added pipe.
        """
        pipe_id = self.generate_unique_id(edge_id)
        self.wn.add_pipe(pipe_id, start_node_id, end_node_id, length=length, diameter=diameter, roughness=roughness)
        return pipe_id

    def create_graph(self, graph):
        """
        Processes a batch of results from Neo4j query and adds corresponding nodes and pipes to the water network model.

        Parameters:
            graph (list): List of results from Neo4j query.
        """
        for attributes in graph:
            start = attributes[1]._start_node
            coordinates = self.convert_coords(start['coords_27700'])
            start_id = start._id
            elevation = self.generate_random_value(20, 40)  # Example elevation range
            base_demand = self.generate_random_value(10, 50)  # Example demand range
            start_node_id = self.add_node(start_id, coordinates, elevation, base_demand)

            end = attributes[1]._end_node
            coordinates = self.convert_coords(end['coords_27700'])
            end_id = end._id
            elevation = self.generate_random_value(20, 40)  # Example elevation range
            base_demand = self.generate_random_value(10, 50)  # Example demand range
            end_node_id = self.add_node(end_id, coordinates, elevation, base_demand)

            edge_id = attributes[1]._id
            diameter = attributes[1].get('diameter', 0.1)  # Default diameter
            length = attributes[1].get('segment_length', 1.0)  # Default length
            roughness = self.roughness_values.get(attributes[1].get('material'), 120)
            self.add_pipe(edge_id, start_node_id, end_node_id, diameter, length, roughness)

        return self.wn
