import networkit as nk
from cleanwater.calculators import GisToGraphCalculator

class GisToNkCalculator(GisToGraphCalculator):

    def __init__(self, config):
        self.config = config
        self.G: Graph = nk.Graph(edgesIndexed=True)
        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

        super().__init__(
            self.config.srid,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )


    def create_nk_graph(self) -> None:

        print(self.all_nodes_by_pipe)
        print(self.all_edges_by_pipe)