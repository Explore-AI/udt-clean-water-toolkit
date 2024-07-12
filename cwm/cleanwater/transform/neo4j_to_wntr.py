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
        self.roughness_values = self.load_roughness_values('material_roughness2.csv')

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

    def add_junction(self, id, coordinates):
        """
        Adds a node to the water network model.

        Parameters:
            id (str): ID of the node.
            coordinates (tuple): Coordinates of the node.

        Returns:
            node_id (str): SQIDS ID of the added node.
        """
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = self.generate_random_value(10, 50)  # Example demand range
        self.wn.add_junction(id, elevation=elevation, base_demand=base_demand, coordinates=coordinates)

    def add_valve(self, valve_link_id, new_start_node_id, new_end_node_id, diameter, valve_type):
        """
        Add a valve to the Water Network Toolkit (WNTR) model.

        Parameters:
            valve_link_id: Unique ID for the valve link.
            new_start_node_id: ID of the new start node for the valve.
            new_end_node_id: ID of the new end node for the valve.
            diameter: Diameter of the valve.
            valve_type: Type of the valve.
        """
        self.wn.add_valve(valve_link_id,
                          new_start_node_id,
                          new_end_node_id,
                          diameter,
                          valve_type,
                          initial_status='OPEN')

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