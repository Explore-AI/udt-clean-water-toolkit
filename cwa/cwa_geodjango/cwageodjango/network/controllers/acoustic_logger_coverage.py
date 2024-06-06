from cwageodjango.network.models import *
from neomodel import db
import csv
import pandas as pd

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
        
    def initialise_csv(self):
        with open(self.config.outputfile, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['logger_node_key','pipe_id','pipe_material', 'pipe_diameter',
                             'pipe_length', 'coverage_length','pipe_wkt',
                             'start_node_key','start_node_coords','end_node_key', 
                             'end_node_coords'])

    def get_connected(self, node_key, max_level):
        cypher_query = f"""
        MATCH (logger:NetworkNode{{node_key:'{node_key}'}})
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
                n.coords_27700 AS startNodeCoords,
                m.node_key AS endNodeKey,
                m.coords_27700 as endNodeCoords, 
                r.material AS PipeMaterial,
                r.segment_length AS PipeLength,
                r.segment_wkt AS PipeWkt
            SET r.coveredbyLogger = newCoveredByLogger,
                r.coverageLen = newCoverageLen
            RETURN id(r) AS pipe_id, '{coverage_len}' AS coverage_length, startNodeKey, startNodeCoords, endNodeKey, endNodeCoords, PipeMaterial, PipeLength, PipeWkt 
            """
            results, _ = db.cypher_query(query)

            with open(self.config.outputfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                for result in results:
                    pipe_id = result[0]
                    coverage_length = result[1]
                    start_node_key = result[2]
                    start_node_coords = result[3]
                    end_node_key = result[4]
                    end_node_coords = result[5]
                    pipe_material = result[6]
                    pipe_length = result[7]
                    pipe_wkt = result[8]
                    writer.writerow([logger, pipe_id, pipe_material, pipe_length, coverage_length, pipe_wkt, start_node_key, start_node_coords,
                                     end_node_key, end_node_coords])

    def check_for_pipe_end(self, node_key):
        query = f"MATCH (n {{node_key : '{node_key}'}}) RETURN 'PipeEnd' IN labels(n) AS is_pipe_end"
        results, _ = db.cypher_query(query)
        is_pipe_end_str = results[0][0]
        return is_pipe_end_str
    
    def convert_remaining_distance(self, remaining_distance, current_material, next_material):
        current_material_distance = self.detection_dist.get(current_material)
        next_material_distance = self.detection_dist.get(next_material)
        converted_distance = (remaining_distance / current_material_distance) * next_material_distance
        return converted_distance

    def process_connected_edges(self, node_key, remaining_distance, processed_edges, processed_nodes, pipe_material, logger_key, is_initial):
        if self.check_for_pipe_end(node_key=node_key):
            return

        while remaining_distance > 0:
            processed_nodes.add(node_key)
            next_edges = self.get_next_edges(node_key, processed_edges)

            per_edge_distance = remaining_distance

            for edge in next_edges:
                if 'edge_distance' not in locals() or edge_distance == 0:
                    edge_distance = per_edge_distance
                
                edge_distance = self.convert_remaining_distance(edge_distance, pipe_material, edge[1].get('material'))
                start_node_key = edge[1]._start_node.get('node_key')
                end_node_key = edge[1]._end_node.get('node_key')
                pipe_id = edge[1]._id
                pipe_material = edge[1].get('material')
                pipe_length = edge[1].get('segment_length')

                if pipe_length > edge_distance:
                    covered_distance = edge_distance
                    remaining_distance -= edge_distance
                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                logger_key,
                                                covered_distance)
                    
                    processed_edges.add(pipe_id)
                    edge_distance = 0
                    node_key = end_node_key if start_node_key in processed_nodes else start_node_key

                    if self.check_for_pipe_end(node_key=node_key):
                        edge_distance = 0
                        break

                elif pipe_length <= edge_distance:
                    edge_distance -= pipe_length
                    remaining_distance -= pipe_length  

                    self.update_edge_attributes(start_node_key, 
                                                end_node_key,
                                                logger_key,
                                                pipe_length)

                    processed_edges.add(pipe_id)  

                    if remaining_distance > 0:
                        node_key = end_node_key if start_node_key in processed_nodes else start_node_key
                    
                        if self.check_for_pipe_end(node_key=node_key):
                            remaining_distance -= edge_distance 
                            edge_distance = 0
                            continue

                    if edge_distance > 0 and remaining_distance > 0:
                        is_initial = False
                        self.process_connected_edges(node_key, edge_distance, processed_edges, processed_nodes, pipe_material, logger_key, is_initial)
                    else:
                        break
            else:
                break

    def query_graph_dma(self, dma):
        """
        Generator function to query the graph database for loggers within a specific DMA.

        Parameters:
            dma (str): DMA code to filter loggers.

        Returns:
            results: Result object containing query results.

        """    
        results, m = db.cypher_query(f"MATCH (n) WHERE n.acoustic_logger IS NOT NULL and n.dmas contains '{dma[-1]}' RETURN n")
        return results

    def process_logger(self, loggers):
        for node in loggers:
            key = node[0].get('node_key')
            gid = node[0].get('asset_gids')[0]

            connected_edges = self.get_next_edges(key, set())
            processed_edges = set()
            processed_nodes = set()

            for edge in connected_edges:
                start_node_key = edge[1]._start_node.get('node_key')
                end_node_key = edge[1]._end_node.get('node_key')

                pipe_id = edge[1]._id
                pipe_material = edge[1].get('material')
                pipe_length = edge[1].get('segment_length')
                travel_distance = self.detection_dist.get(pipe_material)

                if pipe_length <= travel_distance:
                    remaining_distance = travel_distance - pipe_length
                    self.update_edge_attributes(start_node_key, end_node_key, key, pipe_length)
                    processed_edges.add(pipe_id)
                    processed_nodes.add(key)

                    if remaining_distance > 0:
                        node_key = end_node_key if start_node_key in processed_nodes else start_node_key
                        self.process_connected_edges(node_key, 
                                                     remaining_distance, 
                                                     processed_edges,
                                                     processed_nodes,
                                                     pipe_material,
                                                     logger_key=key,
                                                     is_initial=False)
                elif pipe_length > travel_distance:
                    covered_distance = pipe_length - travel_distance
                    self.update_edge_attributes(start_node_key, end_node_key, key, travel_distance)
                    continue

    def query_total_pipe_lengths_dma(self, dma):
        results, m = db.cypher_query(f"MATCH (n)-[r]-(m) WHERE n.dmas contains '{dma[-1]}' RETURN sum(r.segment_length);")
        return results

    def summary_statistics(self, outputfile):
        df = pd.read_csv(outputfile, header=[0])
        dma = self.config.dma_codes[-1]
        total_pipe_lengths = self.query_total_pipe_lengths_dma(self.config.dma_codes)[0][0]
        total_pipe_lengths_covered = 0
        for pipe in df.pipe_id.unique():
            dftmp = df.loc[df['pipe_id'] == pipe]
            dftmp = dftmp.drop_duplicates()
            if len(dftmp) > 1:
                pipe_len = dftmp['pipe_length'].iloc[0]
                pipe_cov = dftmp['coverage_length'].sum()
                total_cov = pipe_cov if pipe_cov < pipe_len else pipe_len
                total_pipe_lengths_covered += total_cov
            else:
                total_pipe_lengths_covered += dftmp['coverage_length'].iloc[0]
        precentage_coverage = (total_pipe_lengths_covered/total_pipe_lengths)*100
        summary_file = str('_summary.csv').join(self.config.outputfile.split('.csv'))
        with open(summary_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['dma','total_pipe_lengths','total_pipe_lenghts_covered',
                             'percentage_covered'])
            writer.writerow([dma, total_pipe_lengths, total_pipe_lengths_covered, precentage_coverage])

    def update_edge_coverage_fraction(self, outputfile):
        df = pd.read_csv(outputfile, header=[0])
        for pipe in df.pipe_id.unique():
            dftmp = df.loc[df['pipe_id'] == pipe]
            dftmp = dftmp.drop_duplicates()
            pipe_len = dftmp['pipe_length'].iloc[0]
            if len(dftmp) > 1:
                pipe_cov = dftmp['coverage_length'].sum()
                total_cov = pipe_cov if pipe_cov < pipe_len else pipe_len
            else:
                total_cov = dftmp['coverage_length'].iloc[0]

            start_node_key = dftmp['start_node_key'].iloc[0]
            end_node_key = dftmp['end_node_key'].iloc[0]
            if pipe_len>0:
                cov_fraction = (total_cov / pipe_len)*100
            else:
                cov_fraction = 100
            query = f"""
            MATCH (n {{node_key: '{start_node_key}'}})-[r]-(m {{node_key: '{end_node_key}'}}) 
            SET r.coverageFraction = '{cov_fraction}';
            """
            db.cypher_query(query)

    def compute_cov(self):
        """
        Compute coverage.

        """
        sub_graph = self.query_graph_dma(self.config.dma_codes)

        self.initialise_csv()
        
        self.process_logger(sub_graph)
        
        self.update_edge_coverage_fraction(self.config.outputfile)

        self.summary_statistics(self.config.outputfile)

        




