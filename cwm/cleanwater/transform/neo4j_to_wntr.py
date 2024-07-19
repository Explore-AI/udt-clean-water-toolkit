import networkx as nx
import numpy as np
import pandas as pd
from wntr import network

class Neo4j2Wntr:
    """
    Convert a Neo4j graph the to Water Network Toolkit (WNTR) format.
    """

    def __init__(self, config):
        self.config = config
        self.wn = network.WaterNetworkModel()
        self.wn.options.hydraulic.demand_model = 'DDA'
        self.wn.options.hydraulic.accuracy = 0.001
        self.wn.options.time.duration = self.config.wntr_simulation_length_hours * 3600  # hours
        self.wn.options.time.hydraulic_timestep = self.config.wntr_simulation_timestep_hours * 3600  # hours
        self.wn.options.time.report_timestep = self.config.wntr_simulation_timestep_hours * 3600  # 1 hour
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

    # def generate_unique_id(self, input_string):
    #     """
    #     Generates a unique ID for the given input string.
    #
    #     Parameters:
    #         input_string (str): Input string for which the unique ID is generated.
    #
    #     Returns:
    #         unique_id (str): Unique ID generated using SQID encoding.
    #
    #     """
    #     unique_id = self.sqids.encode([input_string])
    #     return str(unique_id)

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

    def add_node(self, node_id_str, coordinates, node_type):
        """
        Adds a node to the water network model.

        Parameters:
            node_id (int): ID of the node.
            coordinates (tuple): Coordinates of the node.
            node_type (dict): Labels denoting node type(s)

        Returns:
            node_id (str): SQIDS ID of the added node.
        """
        if node_type:
            is_meter = [item for item in node_type if item.endswith('Meter')]
            if is_meter:
                self.add_consumption_junction(node_id_str, coordinates)
            elif "OperationalSite" in node_type:
                self.add_reservoir(node_id_str, coordinates)
            else:
                self.add_junction(node_id_str, coordinates)
        else:
            self.add_junction(node_id_str, coordinates)

    def add_consumption_junction(self, node_id_str, coordinates):
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = self.generate_random_value(10, 50)  # Example demand range
        self.wn.add_junction(node_id_str,
                             elevation=elevation,
                             base_demand=base_demand,
                             coordinates=coordinates)

    def add_junction(self, node_id_str, coordinates):
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = 0  # non-consumption junction
        self.wn.add_junction(node_id_str,
                             elevation=elevation,
                             base_demand=base_demand,
                             coordinates=coordinates)

    def add_reservoir(self, node_id_str, coordinates):
        base_head = 20.0  # Example base head
        self.wn.add_reservoir(node_id_str, base_head=base_head, coordinates=coordinates)

    def add_pipe(self, edge_id, start_node_id, end_node_id, diameter, length, roughness):
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
        pipe_id = edge_id
        start_node_id = start_node_id
        end_node_id = end_node_id
        self.wn.add_pipe(
            pipe_id,
            start_node_id,
            end_node_id,
            length=length,
            diameter=diameter,
            roughness=roughness)

    def check_graph_completeness(self):
        self.keep_largest_component()
        node_ids_queried = [str(node._id) for node in self.nodes_loaded]
        node_ids_added = self.wn.node_name_list
        missing_nodes = set(node_ids_queried) - set(node_ids_added)
        if missing_nodes:
            print(f"{len(missing_nodes)} nodes excluded: {missing_nodes}")
        else:
            print("All queried nodes added to WN")

        link_ids_queried = [str(link._id) for link in self.links_loaded]
        link_ids_added = self.wn.link_name_list
        missing_links = set(link_ids_queried) - set(link_ids_added)
        if missing_links:
            print(f"{len(missing_links)} links excluded: {missing_links}")
        else:
            print("All queried edges added to WN")

    def keep_largest_component(self):
        # Create an undirected graph from the water network model
        G = self.wn.to_graph().to_undirected()

        # Find all connected components
        connected_components = list(nx.connected_components(G))

        # Identify the largest connected component
        largest_component = max(connected_components, key=len)

        # Find nodes to remove
        nodes_to_remove = set(G.nodes()) - largest_component

        # Find links to remove (links connected to nodes_to_remove)
        links_to_remove = []
        for link_name, link in self.wn.links():
            if link.start_node_name in nodes_to_remove or link.end_node_name in nodes_to_remove:
                links_to_remove.append(link_name)

        # Remove links from the water network model
        for link_name in links_to_remove:
            self.wn.remove_link(link_name)

        # Remove nodes from the water network model
        for node_name in nodes_to_remove:
            self.wn.remove_node(node_name)







