from rest_framework import viewsets, status
from rest_framework.response import Response
from neomodel import db

from django.contrib.gis.geos import Point


class SchematicViewset(viewsets.ViewSet):
    http_method_names = ["get"]

    @staticmethod
    def query_by_dma(request):

        limit = request.query_params.get("limit", 10)
        dma_code = request.query_params.get("dma_code", 'ZCHIPO01')
        #ZMAIDL45
        if dma_code:
            query = f"""
            match (n:NetworkNode)-[r:PipeMain]->(m:NetworkNode)
            match (n)-[r1]-(d:DMA) where d.code = 'ZCHIPO01'
            return ID(n), n, ID(r), r, ID(m), m
            limit {limit}
            """

            results, _ = db.cypher_query(query)

            return results
        else:
            return []

    def create_node(self, node_id, position, node_type="default", properties={}):

        # point = Point(position[0], position[1], srid=27700)

        # point_4326 = point.transform(4326, clone=True)

        return {
            "id": node_id,
            "key": node_id,
            "type": node_type,
            "position": {
                # "x": point_4326.x,
                # "y": point_4326.y,
                "x": position[0] * 10,
                "y": position[1] * 10,
            },
            "data": {"label": node_id, **properties},
        }

    def create_edge(self, edge_id, from_node_id, to_node_id):

        return {
            "id": edge_id,
            "key": edge_id,
            "source": str(from_node_id),
            "target": str(to_node_id),
            "type": "straight",
            "style": {"strokeWidth": "5px", "color": "black"},
        }

    def find_start_end_node_on_edge(
        self, start_node_id, start_node_data, end_node_id, end_node_data, line_coords
    ):
        """We need to check if the line terminal points are the same as the
        node points to get them in the correct order
        We don't want to compare the coordinates directly becuase of roundlng errors
        We therefore check if the points are the same."""

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
            node_type="circle",
            properties=start_node_data._properties,
        )
        end_node = self.create_node(
            end_node_id,
            end_node_data["coords_27700"],
            node_type="circle",
            properties=end_node_data._properties,
        )

        if point1 != point2:
            end_node, start_node = start_node, end_node

        return start_node, end_node

    def create_nodes(self, item, node_ids):

        start_node_id = str(item[0])
        start_node_data = item[1]

        end_node_id = str(item[4])
        end_node_data = item[5]

        edge_id = str(item[2])
        edge_data = item[3]

        segment_wkt = edge_data.get("segment_wkt")
        line_coords_str = segment_wkt.split("(")[1][:-1]
        line_coords = [coord.strip() for coord in line_coords_str.split(",")]

        start_node, end_node = self.find_start_end_node_on_edge(
            start_node_id, start_node_data, end_node_id, end_node_data, line_coords
        )

        new_nodes = []
        if start_node["id"] not in node_ids:
            node_ids.append(start_node["id"])
            new_nodes.append(start_node)

        all_nodes = [start_node]
        for i, coord in enumerate(line_coords[1:-1]):
            node_id = f"{edge_id}-{str(i)}"

            position = [
                float(coord.split(" ")[0]),
                float(coord.split(" ")[1]),
            ]
            edge_node = self.create_node(node_id, position, node_type="edge_node")

            all_nodes.append(edge_node)

            if node_id not in node_ids:
                node_ids.append(node_id)
                new_nodes.append(edge_node)

        all_nodes.append(end_node)

        if end_node["id"] not in node_ids:
            node_ids.append(end_node["id"])
            new_nodes.append(end_node)

        return new_nodes, all_nodes, node_ids

    def create_edges(self, nodes, edge_ids):
        edges = []

        from_node = nodes[0]
        # print()
        # print(pd.DataFrame(nodes))
        # print()
        # import pdb

        # pdb.set_trace()
        for to_node in nodes[1:]:
            from_node_id = from_node["id"]
            to_node_id = to_node["id"]

            edge_id = f"{from_node_id}_{to_node_id}"

            if edge_id in edge_ids:
                continue

            edge = self.create_edge(edge_id, from_node_id, to_node_id)

            edges.append(edge)
            edge_ids.append(edge_id)

            from_node = to_node

        # print()
        # print(pd.DataFrame(edges))
        # print()
        # import pdb

        # pdb.set_trace()

        return edges, edge_ids

    def create_nodes_and_edges(self, item, node_ids, edge_ids):

        new_nodes, all_nodes, node_ids = self.create_nodes(item, node_ids)
        edges, edge_ids = self.create_edges(all_nodes, edge_ids)

        return new_nodes, edges, node_ids, edge_ids

    def get_nodes_edges(self, graph_data):

        # TODO: cleanup as performing redundant operations
        node_ids = []
        edge_ids = []
        all_nodes = []
        all_edges = []

        for item in graph_data:
            nodes, edges, node_ids, edge_ids = self.create_nodes_and_edges(
                item, node_ids, edge_ids
            )
            all_nodes.extend(nodes)
            all_edges.extend(edges)

        return {"nodes": all_nodes, "edges": all_edges}

    def list(self, request):
        data = self.query_by_dma(request)
        n_e = self.get_nodes_edges(data)

        return Response(n_e, status=status.HTTP_200_OK)
