import pdb

import numpy as np
import pandas as pd
from wntr import network
from wntr.network import TimeSeries, Reservoir


class Neo4j2Wntr:
    """
    Convert a Neo4j graph the to Water Network Toolkit (WNTR) format.

    """
    def __init__(self, sqids):
        self.wn = network.WaterNetworkModel()
        self.wn.options.hydraulic.inpfile_units = 'LPS'  # Litres per second
        self.wn.add_pattern('pat1', [1])
        self.wn.add_pattern('pat2', [1, 2, 3, 4])
        self.sqids = sqids
        self.roughness_values = self.load_roughness_values('material_roughness.csv')

    @staticmethod
    def load_roughness_values(csv_path):
        """
        Load roughness values from a CSV file into a dictionary.

        Parameters:
            csv_path (str): Path to the CSV file.

        Returns:
            dict: Dictionary with material types as keys and roughness values as values.
        """
        df = pd.read_csv(csv_path)
        roughness_dict = pd.Series(df.roughness.values, index=df.material).to_dict()
        return roughness_dict

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

    def add_reservoir(self, node_name, coordinates):
        """
        Adds a node to the water network model.

        Parameters:
            node_name (str): ID of the node.
            coordinates (tuple): EPSG:27700 coordinates of the node.

        Returns:
            node_id (str): SQIDS ID of the added node.

        """
        node_id = self.generate_unique_id(node_name)

        reservoir = Reservoir(name=node_id, wn=self.wn, base_head=20, head_pattern='pat1')
        reservoir._coordinates = coordinates
        print(reservoir.name)
        self.wn.add_reservoir(reservoir)

        # self.wn.add_reservoir(node_id,
        #                       base_head=20,
        #                       coordinates=coordinates,
        #                       head_pattern='pat1'
        #                       )
        print("created reservoir")


        return node_id

    def add_node(self, node_name, coordinates):
        """
        Adds a node to the water network model.

        Parameters:
            node_name (str): ID of the node.
            coordinates (tuple): EPSG:27700 coordinates of the node.

        Returns:
            node_id (str): SQIDS ID of the added node.

        """
        node_id = self.generate_unique_id(node_name)

        generate_elevation = lambda: np.random.uniform(20, 40)  # replace with actual values
        generate_base_demand = lambda: np.random.uniform(10, 50)  # replace with actual values

        self.wn.add_junction(
            node_id,
            base_demand=generate_base_demand(),
            elevation=generate_elevation(),
            coordinates=coordinates
        )

        return node_id

    def add_pipe(self, edge_id, start_node_id, end_node_id, length, diameter, material):
        """
        Adds a pipe to the water network model.

        Parameters:
            edge_id (str): ID of the edge (pipe).
            start_node_id (str): ID of the start node.
            end_node_id (str): ID of the end node.
            diameter (flt): diameter in mm of pipe.
            material (str): material of pipe.
            length (flt): length of pipe.

        Returns:
            pipe_id (str): SQIDS ID of the added pipe.

        """
        pipe_id = self.generate_unique_id(edge_id)

        roughness = self.roughness_values.get(material, None)

        if roughness is None:
            print(f"Material '{material}' not found in roughness data. Using default roughness.")
            roughness = 120  # Default roughness value if material is not found

        self.wn.add_pipe(pipe_id, start_node_id, end_node_id, length, diameter, roughness)

        return pipe_id

    def create_graph(self, graph):
        """
        Processes a batch of results from Neo4j query and adds corresponding nodes and pipes to the water network model.

        Parameters:
            batch_result (list): List of results from Neo4j query.

        """
        count = 0
        for attributes in graph:
            count += 1
            if count == 123:
                start = attributes[1]._start_node
                start_coords = start['coords_27700']
                start_id = start._id

                # Validate start node coordinates
                if start_coords is None:
                    print(f"Start node {start_id} has invalid coordinates: {start_coords}")
                    continue

                start_node_id = self.add_reservoir(start_id, start_coords)

                end = attributes[1]._end_node

                end_coords = end['coords_27700']
                end_id = end._id

                # Validate end node coordinates
                if end_coords is None:
                    print(f"End node {end_id} has invalid coordinates: {end_coords}")
                    continue

                count += 1
                end_node_id = self.add_node(end_id, end_coords)

                edge_id = attributes[1]._id
                edge_material = attributes[1]['material']
                edge_diameter = attributes[1]['diameter']
                edge_length = attributes[1]['segment_length']
                self.add_pipe(edge_id, start_node_id, end_node_id, edge_length, edge_diameter, edge_material)

            else:
                start = attributes[1]._start_node
                start_coords = start['coords_27700']
                start_id = start._id

                # Validate start node coordinates
                if start_coords is None:
                    print(f"Start node {start_id} has invalid coordinates: {start_coords}")
                    continue

                start_node_id = self.add_node(start_id, start_coords)

                end = attributes[1]._end_node

                end_coords = end['coords_27700']
                end_id = end._id

                # Validate end node coordinates
                if end_coords is None:
                    print(f"End node {end_id} has invalid coordinates: {end_coords}")
                    continue

                count += 1
                end_node_id = self.add_node(end_id, end_coords)

                edge_id = attributes[1]._id
                edge_material = attributes[1]['material']
                edge_diameter = attributes[1]['diameter']
                edge_length = attributes[1]['segment_length']
                self.add_pipe(edge_id, start_node_id, end_node_id, edge_length, edge_diameter, edge_material)

        return self.wn
