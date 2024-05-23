from rest_framework import viewsets, status
from rest_framework.response import Response
from neomodel import db


class SchematicViewset(viewsets.ViewSet):
    http_method_names = ["get"]

    @staticmethod
    def query_by_dma(request):
        dma_code = request.query_params.get("dma_code")
        if dma_code:
            query = f"match (n)-[r]-(m) where n.dmas contains '{dma_code}' return ID(n), n, ID(r), r, ID(m), m limit 6"
            results, _ = db.cypher_query(query)
            return results
        else:
            return []

    @staticmethod
    def create_edge(edge_id, start_node_id, end_node_id):
        return {
            "id": str(edge_id),
            "key": edge_id,
            "source": str(start_node_id),
            "target": str(end_node_id),
            #            "style": {"strokeWidth": 2},
        }

    @staticmethod
    def create_node(node_id, node_data):

        return {
            "id": str(node_id),
            "key": node_id,
            "type": "circle",
            "position": {
                "x": node_data["coords_27700"][0],
                "y": node_data["coords_27700"][1],
            },
            "data": {"label": node_id},
        }

    def create_nodes_edges(self, data):

        node_ids = []
        edge_ids = []
        nodes = []
        edges = []

        # TODO: cleanup as performing redundant operations
        for i in data:
            start_node = self.create_node(i[0], i[1])
            end_node = self.create_node(i[4], i[5])
            edge = self.create_edge(i[2], start_node["id"], end_node["id"])

            if i[0] not in node_ids:
                node_ids.append(i[0])
                nodes.append(start_node)

            if i[4] not in node_ids:
                node_ids.append(i[4])
                nodes.append(end_node)

            if i[2] not in edge_ids:
                edge_ids.append(i[2])
                edges.append(edge)

        return {"nodes": nodes, "edges": edges}

    def list(self, request):
        data = self.query_by_dma(request)
        n_e = self.create_nodes_edges(data)
        return Response(n_e, status=status.HTTP_200_OK)
