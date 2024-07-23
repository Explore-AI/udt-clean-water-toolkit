import pdb

import networkx as nx
import numpy as np
import pandas as pd
import wntr
from wntr import network


class Neo4j2Wntr:
    """
    Convert a Neo4j graph to Water Network Toolkit (WNTR) format.
    """

    def __init__(self, config):
        self.config = config
        self.wn = wntr.network.WaterNetworkModel()

        # Set default hydraulic options
        self.set_hydraulic_options()

        # Set simulation time options
        self.set_simulation_time_options()

        # Load roughness values
        self.roughness_values = self.load_roughness_values('material_roughness2.csv')

    def set_simulation_time_options(self):
        self.wn.options.time.duration = self.config.wntr_simulation_length_hours * 3600
        self.wn.options.time.hydraulic_timestep = self.config.wntr_simulation_timestep_hours * 3600
        self.wn.options.time.pattern_timestep = self.config.wntr_simulation_timestep_hours * 3600
        self.wn.options.time.report_timestep = self.config.wntr_simulation_timestep_hours * 3600

    def set_hydraulic_options(self):
        self.wn.options.hydraulic.demand_model = 'DDA'
        self.wn.options.hydraulic.accuracy = 0.001
        self.wn.options.hydraulic.headloss = 'H-W'  # Example: Hazen-Williams
        self.wn.options.hydraulic.minimum_pressure = 0.0
        self.wn.options.hydraulic.required_pressure = 0.07
        self.wn.options.hydraulic.pressure_exponent = 0.5
        self.wn.options.hydraulic.emitter_exponent = 0.5
        self.wn.options.hydraulic.trials = 200
        self.wn.options.hydraulic.unbalanced = 'STOP'
        self.wn.options.hydraulic.checkfreq = 2
        self.wn.options.hydraulic.maxcheck = 10
        self.wn.options.hydraulic.damplimit = 0.0
        self.wn.options.hydraulic.headerror = 0.0
        self.wn.options.hydraulic.flowchange = 0.0
        self.wn.options.hydraulic.inpfile_units = 'LPS'
        self.wn.options.hydraulic.inpfile_pressure_units = 'LPS'

    def set_reaction_options(self):
        self.wn.options.reaction.bulk_order = 1.0
        self.wn.options.reaction.wall_order = 1.0
        self.wn.options.reaction.tank_order = 1.0
        self.wn.options.reaction.bulk_coeff = 0.0
        self.wn.options.reaction.wall_coeff = 0.0
        self.wn.options.reaction.limiting_potential = None
        self.wn.options.reaction.roughness_correl = None

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
        """
        if node_type:
            is_meter = [item for item in node_type if item.endswith('Meter')]
            if is_meter:
                self.add_consumption_junction(node_id_str, coordinates)
            elif "reservoir" in node_type:
                self.add_reservoir(node_id_str, coordinates)
            else:
                self.add_junction(node_id_str, coordinates)
        else:
            self.add_junction(node_id_str, coordinates)

    def add_junction(self, node_id_str, coordinates):
        """
        Adds a non-consumption junction to the network.
        """
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = 0  # non-consumption junction
        self.wn.add_junction(node_id_str,
                             elevation=elevation,
                             base_demand=base_demand,
                             coordinates=coordinates)

    def add_reservoir(self, node_id_str, coordinates):
        """
        Adds a reservoir to the network.
        """
        base_head = 20.0  # Example base head
        self.wn.add_reservoir(node_id_str, base_head=base_head, coordinates=coordinates)

    def add_pipe(self, edge_id, start_node_id, end_node_id, diameter, length, roughness):
        """
        Adds a pipe to the water network model.
        """
        self.wn.add_pipe(
            edge_id,
            start_node_id,
            end_node_id,
            length=length,
            diameter=diameter,
            roughness=roughness
        )

    def add_consumption_junction(self, node_id_str, coordinates):
        """
        Adds a consumption junction to the network and assigns a demand pattern.
        """
        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = self.generate_random_value(10, 50)  # Example demand range
        self.wn.add_junction(node_id_str,
                             elevation=elevation,
                             base_demand=base_demand,
                             coordinates=coordinates)

        # Generate and assign a daily demand pattern
        self.assign_demand_pattern(node_id_str)

    def generate_daily_pattern(self, peak_factor=1.5):
        """
        Generate a daily demand pattern with a given time interval.

        Parameters:
            peak_factor (float): Factor to adjust the peak demand.

        Returns:
            pattern (list): A list of demand factors for each time interval.
        """
        # Number of time steps in a day
        num_steps = int(self.config.wntr_simulation_length_hours / self.config.wntr_simulation_timestep_hours)

        # Create a base pattern with typical daily usage
        base_pattern = np.sin(np.linspace(0, 2 * np.pi, num_steps)) + 1.1  # Sinusoidal pattern with daily peak

        # Normalize to sum to 1 and then scale to typical daily demand (e.g., total demand for a node)
        base_pattern = (base_pattern - np.min(base_pattern)) / (np.max(base_pattern) - np.min(base_pattern))

        # Scale the pattern to include peak demand
        pattern = base_pattern * peak_factor

        return pattern.tolist()

    def assign_demand_pattern(self, node_id_str):
        """
        Create and assign a daily demand pattern to a specific consumption junction.

        Parameters:
            node_id_str (str): The ID of the node to which the pattern will be assigned.
        """
        # Generate the pattern
        pattern_values = self.generate_daily_pattern()
        pattern_name = 'daily_pattern_' + node_id_str

        # Add the pattern to the network model
        self.wn.add_pattern(name=pattern_name, pattern=pattern_values)

        # Create a TimeSeries object with the pattern
        demand_base_value = self.wn.get_node(node_id_str).base_demand

        # Assign the TimeSeries object to the node's demand_timeseries_list
        for demand in self.wn.get_node(node_id_str).demand_timeseries_list:
            demand.base_value = demand_base_value
            demand.pattern_name = pattern_name

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
