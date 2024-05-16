from cwageodjango.network.models import *
from neomodel import db
import csv
import numpy as np

class AcousticLoggerCoverage():
    def __init__(self, config):
        self.config = config
        self.detection_dist = {
                  'ductile_iron':150,
                  'cast_iron':150,
                  'steel':150,
                  'unknown':150,
                  'polyethylene_black_poly':70,
                  'pe80_medium_density_polyethylene':70,
                  'asbestos_cement':70,
                  'unplasticised_polyvinyl_chloride':70,
                  'pe100_high_performance_polyethylene':70,
                  'concrete':70,
                  'glass_reinforced_plastic':70,
                  'molecular_orientated_polyvinyl_chloride':70,
                  'spun_iron':150,
                  'coated_steel':150,
                  'lead':150,
                  'barrier_pipecoated_aluminium':150,
                  'other':70,
                  'poly_vinyl_chloride':70,
                  'brick':70,
                  'galvanised_iron':150,
                  'fibreglass':70,
                  'hpp':70,
                  'alkathene':70,
                  'copper':150,
                  'alloyed_polyvinyl_chloride':70,
                  'biaxial_polyvinyl_chloride':70,
                  'galvanized_steel':150}
    def initialize_csv(self):
        with open(self.config.outputfile, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['logger_node_key', 'pipe_id', 'coverage_length'])

    def get_connected(self, node_key, max_level):
        cypher_query = f"""
        MATCH (logger:PointNode{{node_key:'{node_key}'}})
        CALL apoc.path.subgraphAll(logger, {{
        relationshipFilter : "TrunkMain|DistributionMain",
        minLevel: 0,
        maxLevel: {max_level}
        }})
        YIELD nodes, relationships
        RETURN nodes, relationships
        """
        results, meta = db.cypher_query(cypher_query)
        return results

    def get_next_edges(self, node_key, processed_edges):
        processed_nodes_condition = ""
        if processed_edges:
            processed_nodes_condition = "AND NOT m.node_key IN " + str(list(processed_edges))

        cypher_query = f"""
        MATCH (n {{node_key: '{node_key}'}})-[r]-(m)
        WHERE NOT id(r) IN {list(processed_edges)}
        {processed_nodes_condition}
        RETURN n, r, m
        """
        results, _ = db.cypher_query(cypher_query)
        return results
    

    def update_edge_attributes(self, start_node_key, end_node_key, logger, coverage_len):
            query = f"""
            MATCH (n {{node_key: '{start_node_key}'}})-[r]-(m {{node_key: '{end_node_key}'}})
            WITH r, 
                CASE WHEN r.coveredbyLogger IS NOT NULL THEN r.coveredbyLogger + '|' + '{logger}' ELSE '{logger}' END AS newCoveredByLogger,
                CASE WHEN r.coverageLen IS NOT NULL THEN r.coverageLen + '|' + '{coverage_len}' ELSE '{coverage_len}' END AS newCoverageLen,
                n.node_key AS startNodeKey,
                m.node_key AS endNodeKey
            SET r.coveredbyLogger = newCoveredByLogger,
                r.coverageLen = newCoverageLen
            RETURN id(r) AS pipe_id, '{coverage_len}' AS coverage_length, startNodeKey, endNodeKey
            """
            results, _ = db.cypher_query(query)

            # Log to CSV
            with open(self.config.outputfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                for result in results:
                    pipe_id = result[0]
                    coverage_length = result[1]
                    start_node_key = result[2]
                    end_node_key = result[3]
                    writer.writerow([logger, pipe_id, coverage_length, start_node_key, end_node_key])

    def check_for_pipe_end(self, node_key):
        query = f"MATCH (n {{node_key : '{node_key}'}}) RETURN 'PipeEnd' IN labels(n) AS is_pipe_end"
        results, _ = db.cypher_query(query)
        is_pipe_end_str = results[0][0]  # This might be a string "True" or "False"
        #is_pipe_end = is_pipe_end_str.lower() == "true"  # Convert to boolean
        return is_pipe_end_str

    def process_connected_edges(self, node_key, original_remaining_distance, remaining_distance, processed_edges, logger_key):
        if self.check_for_pipe_end(node_key=node_key):
            print("Node is labeled as PipeEnd. Skipping processing.")
            return    
        while remaining_distance > 0:
            print(f'DISTANCE {remaining_distance}')
            processed_nodes = set()
            processed_nodes.add(node_key)
            next_edges = self.get_next_edges(node_key, processed_edges)
            print(f'Getting next connected edges at {node_key}.')
            for edge in next_edges:
                start_node_key = edge[1]._start_node.get('node_key')
                end_node_key = edge[1]._end_node.get('node_key')

                pipe_id = edge[1]._id
                pipe_material = edge[1].get('material')
                pipe_length = edge[1].get('segment_length')
                travel_distance = self.detection_dist.get(pipe_material)

                if pipe_length <= remaining_distance:
                    remaining_distance -= pipe_length  # Update remaining_distance
                    print(f'Next pipe {pipe_id} covered', 'remaining', remaining_distance)

                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                logger_key,
                                                pipe_length)

                    processed_edges.add(pipe_id)  # Add pipe_id to processed_edges
                    if remaining_distance > 0:

                        if start_node_key in processed_nodes:
                            node_key = end_node_key  # Update node_key for next iteration
                        else:
                            node_key = start_node_key
                        # Check if the current node is a "PipeEnd" node before proceeding
                        if not self.check_for_pipe_end(node_key=node_key):
                            # Proceed with the next connected edges if the current node is not a "PipeEnd" node
                            break
                        else:
                            print("Node is labeled as PipeEnd. Skipping processing.")
                            continue  # Exit the loop and the function
                        
                elif pipe_length > remaining_distance:
                    covered_distance = pipe_length - remaining_distance

                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                logger_key,
                                                remaining_distance)
                    
                    print(f'Whole next pipe {pipe_id} is not covered.', covered_distance, 'of', pipe_length, 
                        'is remaining.')
                    remaining_distance = 0  # Set remaining_distance to 0 since the pipe is longer than remaining distance
                    break  # Exit the loop to get next connected edges
                processed_edges.add(pipe_id)
            else:
                break  # Break out of while loop if remaining_distance is 0 or no more edges to process


    def query_graph_dma(self, dma):
        """
        Generator function to query the graph database for loggers within a specific DMA.

        Parameters:
            dma (str): DMA code to filter loggers.

        Yields:
            results: Result object containing query results.

        """    

        results, m = db.cypher_query(f"MATCH (n) WHERE n.acoustic_logger IS NOT NULL and n.dmas contains '{dma[-1]}' RETURN n limit 10")
        return results

    def process_logger(self, loggers):
        for node in loggers:

            key = node[0].get('node_key')
            

            gid = node[0].get('asset_gids')[0]

            print(f'........Starting with Logger: {key}...........')

            initial_max_level = 1
            max_detection = 300

            connected_edges = self.get_next_edges(key, set())
            processed_edges = set()

            for edge in connected_edges:
                start_node_key = edge[1]._start_node.get('node_key')
                end_node_key = edge[1]._end_node.get('node_key')

                pipe_id = edge[1]._id
                pipe_material = edge[1].get('material')
                pipe_length = edge[1].get('segment_length')
                travel_distance = self.detection_dist.get(pipe_material)

                if pipe_length <= travel_distance:
                    remaining_distance = travel_distance - pipe_length
                    print(f'Pipe {pipe_id} covered', 'remaining', remaining_distance)
                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                key,
                                                pipe_length)
                    processed_edges.add(pipe_id)  # Add pipe_id to processed_edges
                    if remaining_distance > 0:
                        self.process_connected_edges(end_node_key, remaining_distance, remaining_distance, processed_edges, logger_key=key)
                elif pipe_length > travel_distance:
                    covered_distance = pipe_length - travel_distance
                    print(f'Whole pipe {pipe_id} is not covered.', covered_distance, 'of', pipe_length, 'is remaining.')
                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                key,
                                                travel_distance)
                    continue
            print(f'........Finshed with Logger: {key}........')


    def compute_cov(self):
        """
        Converts the Neo4j graph data to WNTR format.

         """
        sub_graph  = self.query_graph_dma(self.config.dma_codes)

        print(type(sub_graph))
        
        self.process_logger(sub_graph)

        




