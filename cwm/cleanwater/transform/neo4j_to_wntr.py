import pdb

from wntr import network
import random


class Neo4j2Wntr:
    """
    Convert a Neo4j graph the to Water Network Toolkit (WNTR) format.
    """

    def __init__(self, sqids):
        self.wn = network.WaterNetworkModel()
        self.sqids = sqids
        self.valve_types = ["PRV", "PSV", "FCV", "TCV"]

    def flatten_list(self, nested_list):
        flattened_list = []
        for item in nested_list:
            if isinstance(item, list):
                flattened_list.extend(self.flatten_list(item))
            else:
                flattened_list.append(item)
        return flattened_list

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
            node_type (str, optional): Type of the node. Defaults to None.

        Returns:
            node_id (str): SQIDS ID of the added node.

        """
        node_id = id

        # if node_type and "NetworkOptValve" in node_type or "PressureControlValve" in node_type:
        #     base_head = random.uniform(80, 120)  # Example head value
        #     self.wn.add_reservoir(node_id, base_head=base_head, coordinates=(x, y))
        # else:
        # Random elevation between 0 and 100 meters
        elevation = random.uniform(0, 100)

        # Random base demand between 0 and 1 cubic meters per second
        base_demand = random.uniform(0, 1)

        self.wn.add_junction(
            node_id,
            base_demand=base_demand,
            elevation=elevation,
            coordinates=(x, y),
        )

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
        pipe_id = edge_id

        # Assigning default values to pipe attributes
        length = random.uniform(100, 1000)  # in meters
        diameter = random.uniform(0.1, 1)  # in meters
        roughness = random.uniform(100, 150)  # Hazen-Williams C-factor

        self.wn.add_pipe(
            pipe_id,
            start_node_id,
            end_node_id,
            length=length,
            diameter=diameter,
            roughness=roughness,
        )

        return pipe_id

    def create_graph(self, network_triads_results, asset_dict):
        """
        Processes results from Neo4j query and adds corresponding nodes and pipes to the water network model.

        Parameters:
            network_nodes_results (list): List of results from Neo4j query for network nodes and pipes.
            asset_dict (dict): Dictionary containing node IDs and their asset labels.

        Returns:
            wn: Updated water network model.
        """
        for triad in network_triads_results:
            edge = triad[1]
            start = edge._start_node
            start_x, start_y = (
                start.get("coords_27700")[0],
                start.get("coords_27700")[1],
            )
            start_id = start._id

            end = edge._end_node
            end_x, end_y = (
                end.get("coords_27700")[0],
                end.get("coords_27700")[1],
            )
            end_id = end._id

            edge_id = edge._id

            # Adding nodes and pipe to self.wn
            start_node_id = self.add_node(str(start_id), start_x, start_y)
            if start_node_id is None:
                print(f"Failed to add node: {start_id}")
                continue

            end_node_id = self.add_node(str(end_id), end_x, end_y)
            if end_node_id is None:
                print(f"Failed to add node: {end_id}")
                continue

            pipe_added = self.add_pipe(str(edge_id), start_node_id, end_node_id)
            if not pipe_added:
                print(f"Failed to add pipe: {edge_id}")
                continue

            # Check if nodes and link are present in self.wn
            if start_node_id not in self.wn.nodes:
                print(f"Node {start_node_id} not found in self.wn")
                continue

            if end_node_id not in self.wn.nodes:
                print(f"Node {end_node_id} not found in self.wn")
                continue

            if edge_id not in self.wn.links:
                print(f"Link {edge_id} not found in self.wn")
                continue

        return self.wn

