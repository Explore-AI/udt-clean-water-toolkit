from rest_framework import viewsets, status
from rest_framework.response import Response
from neomodel import db


class SchematicViewset(viewsets.ViewSet):
    http_method_names = ["get"]
    node_ids = []
    edge_ids = []
    nodes = []
    edges = []

    @staticmethod
    def query_by_dma(request):
        dma_code = request.query_params.get("dma_code")
        if dma_code:
            query = f"""
            match (n)-[r]->(m) where n.dmas
            contains '{dma_code}' return
            ID(n), n, ID(r), r, ID(m), m
            limit 5
            """
            results, _ = db.cypher_query(query)

            return results
        else:
            return []

    def create_node(self, node_id, position, node_type="default"):

        return {
            "id": node_id,
            "key": node_id,
            "type": node_type,
            "position": {
                "x": position[0],#*10,
                "y": position[1],#*10,
            },
            "data": {"label": node_id},
        }

    def create_edge(self, edge_id, from_node_id, to_node_id):

        return {
            "id": edge_id,
            "key": edge_id,
            "source": str(from_node_id),
            "target": str(to_node_id),
            "type": "straight",
            #            "style": {"strokeWidth": 2},
        }

    def create_nodes(self, item):

        start_node_id = str(item[0])
        start_node_data = item[1]

        end_node_id = str(item[4])
        end_node_data = item[5]

        edge_id = str(item[2])
        edge_data = item[3]

        segment_wkt = edge_data.get("segment_wkt")
        line_coords_str = segment_wkt.split("(")[1][:-1]
        line_coords = [coord.strip() for coord in line_coords_str.split(",")]

        start_node = self.create_node(
            start_node_id, start_node_data["coords_27700"], node_type="circle"
        )
        end_node = self.create_node(
            end_node_id, end_node_data["coords_27700"], node_type="circle"
        )

        new_nodes = []

        if start_node_id not in self.node_ids:
            self.node_ids.append(start_node_id)
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

            if node_id not in self.node_ids:
                self.node_ids.append(node_id)
                new_nodes.append(edge_node)

        all_nodes.append(end_node)

        if end_node_id not in self.node_ids:
            self.node_ids.append(end_node_id)
            new_nodes.append(end_node)

        return new_nodes, all_nodes

    def create_edges(self, nodes):
        edges = []

        from_node = nodes[0]
        for to_node in nodes[1:]:
            from_node_id = from_node["id"]
            to_node_id = to_node["id"]

            edge_id = f"{from_node_id}_{to_node_id}"

            if edge_id in self.edge_ids:
                continue

            edge = self.create_edge(edge_id, from_node_id, to_node_id)

            edges.append(edge)
            self.edge_ids.append(edge_id)

            from_node = to_node

        return edges

    def create_nodes_and_edges(self, item):

        new_nodes, all_nodes = self.create_nodes(item)

        edges = self.create_edges(all_nodes)

        self.nodes.extend(new_nodes)
        self.edges.extend(edges)

    def get_nodes_edges(self, graph_data):

        # TODO: cleanup as performing redundant operations
        for item in graph_data:
            self.create_nodes_and_edges(item)

        return {"nodes": self.nodes, "edges": self.edges}

    def list(self, request):
        data = self.query_by_dma(request)
        n_e = self.get_nodes_edges(data)
        return Response(n_e, status=status.HTTP_200_OK)
