import pdb

import numpy as np
import pandas as pd
from wntr import network

class Neo4j2Wntr:
    """
    Convert a Neo4j graph the to Water Network Toolkit (WNTR) format.
    """

    def __init__(self, sqids):
        self.wn = network.WaterNetworkModel()
        self.sqids = sqids
        self.valve_types = ["PRV", "PSV", "FCV", "TCV"]
        self.roughness_values = self.load_roughness_values('material_roughness2.csv')

    @staticmethod
    def convert_coords(coords):
        """
        Helper function to convert coords_27700 to a tuple.
        """
        return tuple(coords)

    def flatten_list(self, nested_list):
        flattened_list = []
        for item in nested_list:
            if isinstance(item, list):
                flattened_list.extend(self.flatten_list(item))
            else:
                flattened_list.append(item)
        return flattened_list

    @staticmethod
    def generate_random_value(min_value, max_value):
        """
        Generate a random value within the specified range.
        """
        return np.random.uniform(min_value, max_value)

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

    def add_node(self, id, coordinates):
        """
        Adds a node to the water network model.

        Parameters:
            id (str): ID of the node.
            coordinates (tuple): Coordinates of the node.

        Returns:
            node_id (str): SQIDS ID of the added node.
        """
        node_id = str(id)
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = self.generate_random_value(10, 50)  # Example demand range
        self.wn.add_junction(node_id, elevation=elevation, base_demand=base_demand, coordinates=coordinates)

    def add_pipe(self, edge_id, start_node_id, end_node_id, diameter, length):
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
        pipe_id = str(edge_id)
        start_node_id = str(start_node_id)
        end_node_id = str(end_node_id)
        roughness = 120.0
        self.wn.add_pipe(
            pipe_id,
            start_node_id,
            end_node_id,
            length=length,
            diameter=diameter,
            roughness=roughness)





