import networkit as nk


class Neo4jToNk:
    values_to_drop = ["PointAsset", "PointNode"]

    def __init__(self):
        self.G = nk.Graph(edgesIndexed=True)
        self.edgelabel = self.G.attachEdgeAttribute("label", str)
        self.edgegid = self.G.attachEdgeAttribute("gid", str)
        self.nodelabel = self.G.attachNodeAttribute("label", str)

    def add_pipe(self, start_node_id, end_node_id):
        self.G.addEdge(start_node_id, end_node_id, addMissing=True)

    def get_node_attributes(self, node_type, attribute):
        node = getattr(attribute[1], node_type)

        node_id = node._id
        node_label = [
            x for x in list(node.labels) if attribute not in self.values_to_drop
        ][0]

        self.nodelabel[node_id] = node_label

        return node_id

    def set_edge_attributes(self, start_node_id, end_node_id, attribute):
        # edge_id = attribute[1]._id
        edge_label = attribute[1].type
        edge_gid = str(attribute[1]["gid"])

        self.edgelabel[start_node_id, end_node_id] = edge_label
        self.edgegid[start_node_id, end_node_id] = edge_gid

    def convert_neo4j_to_nk(self, graph):

        for attribute in graph:

            start_node_id = self.get_node_attributes("_start_node", attribute)
            end_node_id = self.get_node_attributes("_end_node", attribute)

            self.add_pipe(start_node_id, end_node_id)
            self.set_edge_attributes(start_node_id, end_node_id, attribute)
