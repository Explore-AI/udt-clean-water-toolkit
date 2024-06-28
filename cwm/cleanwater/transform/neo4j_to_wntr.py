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
        self.wn.options.hydraulic.inpfile_units = 'LPS'  # Litres per second
        self.wn.add_pattern('pat1', [1])
        self.wn.add_pattern('pat2', [1, 2, 3, 4])
        self.sqids = sqids
        self.roughness_values = self.load_roughness_values('material_roughness.csv')
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types

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
        res_id = self.generate_unique_id(node_name) + 'R'

        self.wn.add_reservoir(res_id,
                              base_head=20,
                              coordinates=coordinates,
                              head_pattern='pat1')
        print("Created reservoir:", res_id)
        return res_id, node_id

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

        generate_elevation = lambda: np.random.uniform(20, 40)  # Example elevation range
        generate_base_demand = lambda: np.random.uniform(10, 50)  # Example demand range

        self.wn.add_junction(
            node_id,
            base_demand=generate_base_demand(),
            elevation=generate_elevation(),
            coordinates=coordinates
        )
        print("Created junction:", node_id)
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
        roughness = self.roughness_values.get(material, 120)  # Default roughness if material not found

        self.wn.add_pipe(pipe_id, start_node_id, end_node_id, length, diameter, roughness)
        print("Created pipe:", pipe_id)
        return pipe_id

    def add_pump(self, pump_name, start_node_id, end_node_id):
        """
        Adds a pump to the water network model.

        Parameters:
            pump_name (str): Name of the pump.
            start_node_id (str): ID of the start node.
            end_node_id (str): ID of the end node.

        Returns:
            pump_id (str): SQIDS ID of the added pump.
        """
        pump_id = self.generate_unique_id(pump_name)
        curve_id = f'Curve_{pump_id}'

        # Creating a pump curve (random realistic values for head and flow)
        head_values = np.random.uniform(10, 50, size=3)  # Example head values
        flow_values = np.random.uniform(0, 200, size=3)  # Example flow values
        self.wn.add_curve(curve_id, head_values, flow_values)

        self.wn.add_pump(pump_id, start_node_id, end_node_id, pump_curve=curve_id)
        print("Created pump:", pump_id)
        return pump_id

    def add_valve(self, valve_name, start_node_id, end_node_id, valve_type=None):
        """
        Adds a valve to the water network model.

        Parameters:
            valve_name (str): Name of the valve.
            start_node_id (str): ID of the start node.
            end_node_id (str): ID of the end node.
            valve_type (str): Type of the valve. If None, a random type is chosen.

        Returns:
            valve_id (str): SQIDS ID of the added valve.
        """
        valve_id = self.generate_unique_id(valve_name)
        if valve_type is None:
            valve_type = np.random.choice(self.valve_types)  # Randomly choose a valve type if not specified
        setting = np.random.uniform(5, 50)  # Example setting value, can be adapted based on valve type

        self.wn.add_valve(valve_id, start_node_id, end_node_id, valve_type, setting)
        print("Created valve:", valve_id, "of type:", valve_type)
        return valve_id

    def add_patterns(self):
        """
        Adds demand and time patterns to the water network model.
        """
        # Example demand patterns (random values)
        demand_pattern_values = np.random.uniform(0.5, 1.5, size=24).tolist()  # Demand pattern over 24 hours
        self.wn.add_pattern('demand_pattern', demand_pattern_values)

        # Example time pattern (random values, representing a day in hours)
        time_pattern_values = np.random.uniform(1, 2, size=24).tolist()  # Multipliers for each hour
        self.wn.add_pattern('time_pattern', time_pattern_values)
        print("Added demand and time patterns.")

    def create_graph(self, graph):
        """
        Processes a batch of results from Neo4j query and adds corresponding nodes and pipes to the water network model.

        Parameters:
            graph (list): List of results from Neo4j query.
        """

        def validate_and_get_node(node):
            """Validates the node and returns its coordinates and ID if valid."""
            coords = node['coords_27700']
            node_id = node._id
            if coords is None:
                print(f"Node {node_id} has invalid coordinates: {coords}")
                return None, None
            return coords, node_id

        def add_node_to_model(node, is_reservoir=False):
            """Adds a node to the model and returns its ID, optionally as a reservoir."""
            coords, node_id = validate_and_get_node(node)
            if not coords:
                return None, None

            if is_reservoir:
                return self.add_reservoir(node_id, coords)
            else:
                return self.add_node(node_id, coords), None

        count = 0
        reservoir_nodes = []

        for attributes in graph:
            edge = attributes[1]
            start_node = edge._start_node
            end_node = edge._end_node

            if count == 123:
                start_node_id, _ = add_node_to_model(start_node)
                end_node_id, res_node_id = add_node_to_model(end_node, is_reservoir=True)
                reservoir_nodes.append(res_node_id)
            else:
                if start_node in reservoir_nodes:
                    start_node_id, _ = self.add_reservoir(start_node._id, start_node['coords_27700'])
                    reservoir_nodes.remove(start_node._id)
                else:
                    start_node_id, _ = add_node_to_model(start_node)

                end_node_id, _ = add_node_to_model(end_node)

            if not start_node_id or not end_node_id:
                continue

            # Add pipe to the model
            edge_id = edge._id
            edge_material = edge['material']
            edge_diameter = edge['diameter'] / 1000  # Assuming diameter conversion
            edge_length = edge['segment_length']
            self.add_pipe(edge_id, start_node_id, end_node_id, edge_length, edge_diameter, edge_material)

            # Randomly add a pump or valve to the model
            if np.random.rand() > 0.7:  # 30% chance to add a pump
                self.add_pump(f'Pump_{count}', start_node_id, end_node_id)
            elif np.random.rand() > 0.5:  # 50% chance to add a valve
                self.add_valve(f'Valve_{count}', start_node_id, end_node_id)

            count += 1

        # Add demand and time patterns to the network
        self.add_patterns()

        return self.wn

# Example usage
# sqids = <Initialize your SQIDS object>
# graph_data = <Load your Neo4j graph data>
# neo4j2wntr = Neo4j2Wntr(sqids)
# wn_model = neo4j2wntr.create_graph(graph_data)

