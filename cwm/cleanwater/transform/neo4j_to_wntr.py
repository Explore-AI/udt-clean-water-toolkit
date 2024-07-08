from collections import defaultdict
import numpy as np
import pandas as pd
from wntr import network


class Neo4j2Wntr:
    """
    Convert a Neo4j graph to the Water Network Toolkit (WNTR) format.
    """

    def __init__(self, sqids):
        self.wn = network.WaterNetworkModel()
        self.sqids = sqids
        self.roughness_values = self.load_roughness_values('material_roughness.csv')
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types
        self.setup_default_options()
        self.node_to_pipes = defaultdict(list)  # Initialize defaultdict for node to pipes mapping

    def setup_default_options(self):
        """
        Set up default simulation options.
        """
        self.wn.options.hydraulic.inpfile_units = 'LPS'  # Litres per second
        self.wn.options.time.duration = 7 * 24 * 3600  # Simulation duration in seconds
        self.wn.options.hydraulic.demand_model = 'PDD'  # Pressure Dependent Demand
        self.wn.options.hydraulic.required_pressure = 20  # m
        self.wn.options.hydraulic.minimum_pressure = 2  # m

        # Default patterns
        self.wn.add_pattern('pat1', [1])
        self.wn.add_pattern('pat2', [1, 2, 3, 4])
        self.wn.add_pattern('pat3', [1, 1, 1, 0, 0, 0, 1, 0, 0.5, 0.5, 0.5, 1])

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

    def generate_unique_id(self, input_string):
        """
        Generates a unique ID for the given input string using SQID encoding.
        """
        unique_id = self.sqids.encode([input_string])
        return str(unique_id)

    def add_reservoir(self, node_name, coordinates):
        """
        Adds a reservoir node to the water network model.
        """
        self.wn.add_reservoir(node_name, base_head=20, coordinates=coordinates, head_pattern='pat1')
        return node_name

    def add_node(self, node_name, coordinates):
        """
        Adds a junction node to the water network model.
        """

        elevation = self.generate_random_value(20, 40)  # Example elevation range
        base_demand = self.generate_random_value(10, 50)  # Example demand range

        self.wn.add_junction(
            node_name,
            base_demand=base_demand,
            elevation=elevation,
            coordinates=coordinates
        )
        return node_name

    def add_pipe(self, edge_id, start_node_id, end_node_id, length, diameter, roughness):
        """
        Adds a pipe to the water network model.
        """

        if not self.validate_pipe_attributes(length, diameter, roughness):
            return None

        self.wn.add_pipe(edge_id, start_node_id, end_node_id, length, diameter, roughness, minor_loss=0.0,
                         initial_status='OPEN', check_valve=False)
        return edge_id

    def add_pump(self, pump_name, start_node_id, end_node_id):
        """
        Adds a pump to the water network model.
        """
        curve_id = self.generate_unique_id(pump_name) + 'c'

        # Creating a pump curve (random realistic values for head and flow)
        head_values = self.generate_random_list(10, 50, size=3)
        flow_values = self.generate_random_list(0, 200, size=3)
        self.wn.add_curve(curve_id, 'HEAD', list(zip(flow_values, head_values)))

        self.wn.add_pump(pump_name, start_node_id, end_node_id, pump_type='HEAD', pump_parameter=curve_id)
        return pump_name

    def add_valve(self, valve_name, start_node_id, end_node_id, diameter, valve_type=None):
        """
        Adds a valve to the water network model.
        """

        if valve_type is None:
            valve_type = np.random.choice(self.valve_types)  # Randomly choose a valve type if not specified
        setting = self.generate_random_value(5, 50)  # Example setting value

        self.wn.add_valve(valve_name, start_node_id, end_node_id, diameter, valve_type)

        return valve_name

    def add_patterns(self):
        """
        Adds demand and time patterns to the water network model.
        """
        # Example demand patterns (random values)
        demand_pattern_values = self.generate_random_list(0.5, 1.5, size=24)  # Demand pattern over 24 hours
        self.wn.add_pattern('demand_pattern', demand_pattern_values)

        # Example time pattern (random values, representing a day in hours)
        time_pattern_values = self.generate_random_list(1, 2, size=24)  # Multipliers for each hour
        self.wn.add_pattern('time_pattern', time_pattern_values)

    @staticmethod
    def convert_coords(coords):
        """
        Helper function to convert coords_27700 to a tuple.
        """
        return tuple(coords)

    def create_graph(self, graph):
        for record in graph:
            node1, relationship, node2 = record

            # Extract nodes' properties
            node1_labels = list(node1.labels)
            node1_props = node1._properties
            node2_labels = list(node2.labels)
            node2_props = node2._properties

            # Extract relationship's properties
            relationship_type = relationship.type
            relationship_props = relationship._properties

            if 'PipeJunction' in node1_labels:
                junction_id = node1_props['node_key']
                self.add_node(junction_id, self.convert_coords(node1_props['coords_27700']))

            if 'PipeJunction' in node2_labels:
                junction_id = node2_props['node_key']
                self.add_node(junction_id, self.convert_coords(node2_props['coords_27700']))

            # Add nodes as junctions if they are PipeEnds
            if 'PipeEnd' in node1_labels:
                junction_id = node1_props['node_key']
                self.add_node(junction_id, self.convert_coords(node1_props['coords_27700']))

            if 'PipeEnd' in node2_labels:
                junction_id = node2_props['node_key']
                self.add_node(junction_id, self.convert_coords(node2_props['coords_27700']))

            # Add relationships as pipes if they are PipeMain
            if relationship_type == 'PipeMain':
                pipe_id = relationship_props['tag']
                start_node_id = node1_props['node_key']
                end_node_id = node2_props['node_key']
                diameter = relationship_props.get('diameter', 0)
                length = relationship_props.get('segment_length', 0)
                roughness = self.roughness_values.get(relationship_props.get('material'), 120)
                self.add_pipe(pipe_id, start_node_id, end_node_id, length, diameter, roughness)

            if relationship_type == 'HAS_ASSET' and (
                    'PressureControlValve' in node1_labels or 'NetworkOptValve' in node1_labels):
                valve_id = node1_props['node_key']
                valve_node_id = node2_props['node_key']  # Assuming node2 is the valve node

                # Retrieve the diameter from a connected pipe (previous pipe)
                diameter = self.get_previous_pipe_diameter(valve_node_id)
                print(diameter)
                valve_type = 'PRV' if 'PressureControlValve' in node1_labels else 'FCV'

                self.add_valve(valve_id, valve_node_id, valve_node_id, diameter, valve_type)

            if relationship_type == 'HAS_ASSET' and (
                    'PressureControlValve' in node2_labels or 'NetworkOptValve' in node2_labels):
                valve_id = node2_props['node_key']
                valve_node_id = node1_props['node_key']  # Assuming node1 is the valve node

                # Retrieve the diameter from a connected pipe (previous pipe)
                diameter = self.get_previous_pipe_diameter(valve_node_id)
                print(diameter)
                valve_type = 'PRV' if 'PressureControlValve' in node2_labels else 'FCV'

                self.add_valve(valve_id, valve_node_id, valve_node_id, diameter, valve_type)

            if relationship_type == 'HAS_ASSET' and 'OperationalSite' in node1_labels:
                reservoir_id = node1_props['node_key']
                coordinates = self.convert_coords(node1_props['coords_27700'])
                self.add_reservoir(reservoir_id, coordinates)

            if relationship_type == 'HAS_ASSET' and 'OperationalSite' in node2_labels:
                reservoir_id = node2_props['node_key']
                coordinates = self.convert_coords(node2_props['coords_27700'])
                self.add_reservoir(reservoir_id, coordinates)

        return self.wn

    def get_previous_pipe_diameter(self, valve_node_id):
        """
        Retrieve diameter from the previous pipe connected to the valve node.
        Assumes that node_to_pipes dictionary is populated with pipe information.
        """

        connected_pipes = self.node_to_pipes.get(valve_node_id, [])

        if connected_pipes:
            # Sort pipes based on some criteria if necessary (e.g., by segment length or tag)
            connected_pipes.sort(key=lambda x: x['segment_length'])  # Example: sorting by segment length

            # Get the diameter of the last connected pipe (previous pipe)
            previous_pipe_diameter = connected_pipes[-1]['diameter']
            return previous_pipe_diameter
        else:
            return None

    @staticmethod
    def validate_pipe_attributes(length, diameter, roughness):
        """
        Validate pipe attributes to ensure they are within realistic and feasible ranges.
        """
        if length <= 0 or diameter <= 0 or roughness <= 0:
            return False
        return True

    @staticmethod
    def generate_random_value(min_value, max_value):
        """
        Generate a random value within the specified range.
        """
        return np.random.uniform(min_value, max_value)

    @staticmethod
    def generate_random_list(min_value, max_value, size=24):
        """
        Generate a list of random values within the specified range.
        """
        return np.random.uniform(min_value, max_value, size).tolist()

    def is_reservoir_node(self, node_id):
        """
        Check if the node is a reservoir.
        """
        return isinstance(self.wn.get_node(node_id), network.Reservoir)
