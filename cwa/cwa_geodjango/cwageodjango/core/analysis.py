import argparse
from cwageodjango.core.conf import AppConf
from cwageodjango.network.controllers import (
    GisToNeo4jController,
    GisToNxController,
    GisToNkController,
    InpToNeo4jController,
    Convert2Wntr,
    Neo4jToNkController,
    AcousticLoggerCoverage,
)


class Analysis(AppConf):
    def __init__(self):
        args = self._set_args()
        super().__init__(args.file)

    def _set_args(self):
        parser = argparse.ArgumentParser(
            description="Run Clean Water Toolkit functions"
        )

        parser.add_argument("-f", "--file")

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
        gis_to_neo4j.create_network()

    def cleanwater_gis2networkit(self) -> None:
        gis_to_nk = GisToNkController(self.validated_config)
        gis_to_nk.create_network()
        gis_to_nk.nk_to_graphml()

    def neo4j_to_wntr_inp(self) -> None:
        """
        Converts data from Neo4j to Water Network Toolkit (WNTR) INP format and exports it.

        Uses the Convert2Wntr class to convert the data and export it to INP format.

        Returns:
            None

        """
        convert2wntr = Convert2Wntr(self.validated_config)
        convert2wntr.convert()
        convert2wntr.wntr_to_inp()

    def neo4j_to_wntr_json(self) -> None:
        """
        Converts data from Neo4j to Water Network Toolkit (WNTR) JSON format and exports it.

        Uses the Convert2Wntr class to convert the data and export it to JSON format.

        Returns:
            None

        """
        convert2wntr = Convert2Wntr(self.validated_config)
        convert2wntr.convert()
        convert2wntr.wntr_to_json()

    def inp_to_neo4j(self) -> None:
        convert2neo4j = InpToNeo4jController(self.validated_config)
        convert2neo4j.convert()

    def neo4j_to_networkit_graphml(self) -> None:
        convert2networkit = Neo4jToNkController(self.validated_config)
        convert2networkit.convert()
        convert2networkit.export_graphml()

    def calc_acoustic_coverage(self):
        acoustic_coverage = AcousticLoggerCoverage(self.validated_config)
        acoustic_coverage.compute_cov()

    def _get_run_methods(self):

        return {
            "gis2nx": self.cleanwater_gis2nx,
            "gis2neo4j": self.cleanwater_gis2neo4j,
            "gis2nk": self.cleanwater_gis2networkit,
            "neo4j2wntrinp": self.neo4j_to_wntr_inp,
            "neo4j2wntrjson": self.neo4j_to_wntr_json,
            "neo4j2networkitgraphml": self.neo4j_to_networkit_graphml,
            "networkcoverage": self.calc_acoustic_coverage,
            "inp2neo4j": self.inp_to_neo4j,
        }

    @property
    def _run_method(self):
        methods = self._get_run_methods()
        return methods[self.validated_config.method]
