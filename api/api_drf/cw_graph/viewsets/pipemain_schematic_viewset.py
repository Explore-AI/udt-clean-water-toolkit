# create an api that filters based on the PipekMains
from rest_framework import viewsets, status
from rest_framework.response import Response
from neomodel import db
from django.contrib.gis.geos import Point
from random import randint
from cwageodjango.utilities.models import DMA


ABSTRACT_NODE_LABELS = ["PipeNode", "NetworkNode", "PointAsset"]


class SchematicPipeMainViewset(viewsets.ViewSet):
    http_method_names = ["get"]

    @staticmethod
    def _remove_abstract_node_labels(labels):
        try:
            label = [label for label in labels if label not in ABSTRACT_NODE_LABELS][0]
        except IndexError:
            raise Exception(
                "After removing all asbtract node labels there should only be one node label."
            )
        return label

    @staticmethod
    def query_pipemain_network(request):
        # get all assets connected to the pipemains, as well as the pipemain relationships
        limit = request.query_params.get("limit", 10)
        dma_codes = request.query_params.get(
            "dma_codes", "ZMAIDL45"
        )  # DMA.objects.first().code)
        # ZMAIDL45
        if dma_codes:
            dma_codes = dma_codes.split(",")

        dma_codes = ["ZMAIDL45"]
        query = f"""
        MATCH (d:DMA)-[:IN_DMA]-(n:NetworkNode)-[:IN_UTILITY]-(u:Utility)
        MATCH (n)-[r1:PipeMain]-(s:NetworkNode)
        WHERE d.code IN {dma_codes}
        OPTIONAL MATCH (n)-[r2:HAS_ASSET]->(a)
        return ID(n), n, ID(r1), r1, ID(s), s, ID(a), a, ID(r2), d, u
        limit {limit}
        """

        results, _ = db.cypher_query(query)

        return results

    def create_node(
        self, node_id, position, node_type="default", properties={}, labels=[]
    ):

        point_bng = Point(position[0], position[1], srid=27700)
        # point_4326 = point_bng.transform(4326, clone=True)

        properties["label"] = self._remove_abstract_node_labels(labels)

        return {
            "id": node_id,
            "key": node_id,
            "type": node_type,
            "position": {
                "x": point_bng.x,
                "y": point_bng.y,
                # "x": position[0],
                # "y": position[1],
            },
            "properties": properties,
        }

    def create_edge(
        self,
        edge_id,
        from_node_id,
        to_node_id,
        edge_properties={},
        animated=False,
        label=None,
    ):

        return {
            "id": edge_id,
            "key": edge_id,
            "source": str(from_node_id),
            "target": str(to_node_id),
            "type": "step",
            "label": label,
            "animated": animated,
            "style": {"strokeWidth": "5px", "stroke": "#33658A"},
            "properties": edge_properties,
        }

    def find_start_end_node_on_edge(
        self,
        start_node_id,
        start_node_data,
        end_node_id,
        end_node_data,
        line_coords,
        dma_data,
        utility_data,
    ):
        """We need to check if the line terminal points are the same as the
        node points to get them in the correct order
        We don't want to compare the coordinates directly becuase of roundlng errors
        We therefore check if the Points are the same."""

        point1 = Point(
            start_node_data["coords_27700"][0],
            start_node_data["coords_27700"][1],
            srid=27700,
        )

        position = [
            float(line_coords[0].split(" ")[0]),
            float(line_coords[0].split(" ")[1]),
        ]

        point2 = Point(
            position[0],
            position[1],
            srid=27700,
        )

        start_node = self.create_node(
            start_node_id,
            start_node_data["coords_27700"],
            node_type="pipeNode",
            properties={
                **start_node_data._properties,
                **dma_data._properties,
                "utility": utility_data._properties["name"],
            },  # start_node_data._properties,
            labels=list(start_node_data.labels),
        )
        end_node = self.create_node(
            end_node_id,
            end_node_data["coords_27700"],
            node_type="pipeNode",
            properties={
                **end_node_data._properties,
                **dma_data._properties,
                "utility": utility_data._properties["name"],
            },  # start_node_data._properties,
            labels=list(start_node_data.labels),
        )

        if point1 != point2:
            end_node, start_node = start_node, end_node

        return start_node, end_node

    def create_nodes(self, item, node_ids):

        start_node_id = str(item[0])
        start_node_data = item[1]

        end_node_id = str(item[4])
        end_node_data = item[5]

        edge_data = item[3]

        segment_wkt = edge_data.get("segment_wkt")
        line_coords_str = segment_wkt.split("(")[1][:-1]
        line_coords = [coord.strip() for coord in line_coords_str.split(",")]

        start_node, end_node = self.find_start_end_node_on_edge(
            start_node_id,
            start_node_data,
            end_node_id,
            end_node_data,
            line_coords,
            item[9],
            item[10],
        )

        new_nodes = []
        if start_node["id"] not in node_ids:
            node_ids.append(start_node["id"])
            new_nodes.append(start_node)

        all_nodes = [start_node, end_node]

        if end_node["id"] not in node_ids:
            node_ids.append(end_node["id"])
            new_nodes.append(end_node)

        return new_nodes, all_nodes, node_ids

    def create_edges(self, nodes, edge_ids, edge_data):
        edges = []

        from_node = nodes[0]

        for to_node in nodes[1:]:
            from_node_id = from_node["id"]
            to_node_id = to_node["id"]

            flow_rate = randint(500, 600)
            edge_id = f"{from_node_id}_{to_node_id}"
            edge_properties = {
                "tag": edge_data._properties["tag"],
                "material": edge_data._properties["material"],
                "diameter": edge_data._properties["diameter"],
                "flow_rate": flow_rate,
            }

            if edge_id in edge_ids:
                continue

            edge = self.create_edge(
                edge_id,
                from_node_id,
                to_node_id,
                edge_properties,
                animated=True,
                label=flow_rate,
            )

            edges.append(edge)
            edge_ids.append(edge_id)

            from_node = to_node

        return edges, edge_ids

    def create_asset_node_edge(self, item):
        start_node_id = str(item[0])

        asset_node_id = str(item[6])
        asset_node_data = item[7]

        asset_edge_id = str(item[8])

        asset_node = self.create_node(
            asset_node_id,
            asset_node_data["coords_27700"],
            node_type="assetNode",
            properties=asset_node_data._properties,
            labels=list(asset_node_data.labels),
        )

        asset_edge = self.create_edge(
            asset_edge_id,
            start_node_id,
            asset_node_id,  # edge_type="straight"
        )

        return asset_node, asset_edge

    def create_nodes_and_edges(self, item, node_ids, edge_ids):
        new_nodes, all_nodes, node_ids = self.create_nodes(item, node_ids)
        edges, edge_ids = self.create_edges(all_nodes, edge_ids, edge_data=item[3])

        return new_nodes, edges, node_ids, edge_ids

    def get_nodes_edges(self, data):
        #
        node_ids = []
        edge_ids = []
        all_nodes = []
        all_edges = []

        for item in data:
            nodes, edges, node_ids, edge_ids = self.create_nodes_and_edges(
                item, node_ids, edge_ids
            )
            all_nodes.extend(nodes)
            all_edges.extend(edges)

            asset_id = item[6]
            if asset_id and asset_id not in node_ids:  # if has asset node
                asset_node, asset_edge = self.create_asset_node_edge(item)
                all_nodes.append(asset_node)
                node_ids.append(asset_id)
                all_edges.append(asset_edge)

        return {"nodes": all_nodes, "edges": all_edges}

    def list(self, request):
        results = self.query_pipemain_network(request)
        nodes_edges = self.get_nodes_edges(results)

        return Response(nodes_edges, status=status.HTTP_200_OK)
