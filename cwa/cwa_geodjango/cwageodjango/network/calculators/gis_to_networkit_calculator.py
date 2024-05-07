import networkit as nk
from cleanwater.calculators import GisToGraphCalculator
from cwageodjango.config.settings import sqids

class GisToNkCalculator(GisToGraphCalculator):
    """
    Calculate network graph from geospatial asset data.
    """

    def __init__(self, config):
        self.config = config
        self.G: Graph = nk.Graph(edgesIndexed=True)
        self.edgelabel = self.G.attachEdgeAttribute("label", str)
        self.edgegid = self.G.attachEdgeAttribute("gid", str)
        self.nodelabel = self.G.attachNodeAttribute("label", str)

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []
        self.node_index = {}

        super().__init__(
            self.config.srid,
            sqids,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )

    def add_pipe(self, start_node_id, end_node_id):
        """
        Add a pipe to the network graph.

        Args:
            start_node_id: ID of the starting node of the pipe.
            end_node_id: ID of the ending node of the pipe.

        """
        self.G.addEdge(start_node_id, end_node_id, addMissing=True)

    def create_nk_graph(self) -> None:
        """
        Create a Networkit graph from geospatial asset data.

        Iterates through pipe and node data to construct the network graph with
        appropriate attributes.

        """
        n = 0
        node_index = {}

        for i, pipe in enumerate(self.all_edges_by_pipe):
            from_node_key = pipe[0]['from_node_key']
            to_node_key = pipe[0]['to_node_key']
            edge_gid = pipe[0]['gid']
            
            # Check if from_node_key exists in node_index, if not, assign a new index
            if from_node_key not in self.node_index:
                self.node_index[from_node_key] = len(self.node_index) + 1
            from_node_id = self.node_index[from_node_key]

            # Check if to_node_key exists in node_index, if not, assign a new index
            if to_node_key not in self.node_index:
                self.node_index[to_node_key] = len(self.node_index) + 1
            to_node_id = self.node_index[to_node_key]

            # Add the pipe to the Networkit graph
            self.add_pipe(from_node_id, to_node_id)

            # Add edge attributes
            self.edgelabel[from_node_id, to_node_id] = pipe[0]['asset_label']
            self.edgegid[from_node_id, to_node_id] = str(edge_gid)

            for n in self.all_nodes_by_pipe[i]:
                if n.get('node_key') == from_node_key:
                    self.nodelabel[from_node_id] = n.get('node_labels')[-1]
                elif n.get('node_key') == to_node_key:
                    self.nodelabel[to_node_id] = n.get('node_labels')[-1]