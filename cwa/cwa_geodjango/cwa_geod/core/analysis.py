import argparse
from cwa_geod.core.conf import AppConf
from cwa_geod.network.controllers import GisToNeo4jController, GisToNxController
from cwa_geod.network.controllers import Convert2Wntr

class Analysis(AppConf):
    def __init__(self):
        args = self._set_args()
        super().__init__(args.file)

    def _set_args(self):
        parser = argparse.ArgumentParser(
            description="Run Clean Water Toolkit functions"
        )

        parser.add_argument("-f", "--file")
        parser.add_argument("-o", "--outputfile")

        return parser.parse_args()

    def run(self):
        self._run_method()

    def cleanwater_gis2nx(self) -> None:
        gis_to_nx = GisToNxController(self.validated_config)
        gis_to_nx.create_network()

        # pos = nx.get_node_attributes(nx_graph, "coords")
        # # https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
        # nx.draw(
        #     nx_graph, pos=pos, node_size=10, linewidths=1, font_size=15, with_labels=True
        # )
        # plt.show()

    def cleanwater_gis2neo4j(self) -> None:
        gis_to_neo4j = GisToNeo4jController(self.validated_config)

        if self.validated_config.parallel:
            gis_to_neo4j.create_network_parallel()
        else:
            gis_to_neo4j.create_network()

    def neo4j_to_inp(self) -> None:
        convert2wntr = Convert2Wntr()
        convert2wntr.convert(self.validated_config.batch_size)
        convert2wntr.export_inp(self._set_args().outputfile)

        
    def neo4j_to_json(self) -> None:
        convert2wntr = Convert2Wntr()
        convert2wntr.convert(self.validated_config.batch_size)
        convert2wntr.export_json(self._set_args().outputfile)

    def _get_run_methods(self):

        return {
            "gis2nx": self.cleanwater_gis2nx,
            "gis2neo4j": self.cleanwater_gis2neo4j,
            "neo4j2inp": self.neo4j_to_inp,
            "neo4j2json" : self.neo4j_to_json
        }

    @property
    def _run_method(self):
        methods = self._get_run_methods()
        return methods[self.validated_config.method]
