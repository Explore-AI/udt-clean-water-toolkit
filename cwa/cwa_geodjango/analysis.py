import setup  # Required. Do not remove.
import argparse
from cwa_geod.core.constants import DEFAULT_SRID
from cwa_geod.network.calculators import GisToNetworkX
from cwa_geod.network.calculators import GisToNeo4J


def cleanwater_gis2nx() -> None:
    gis_to_nx = GisToNetworkX(srid=DEFAULT_SRID)
    nx_graph = gis_to_nx.create_network()
    print("Created Graph:", nx_graph)

    # pos = nx.get_node_attributes(nx_graph, "coords")
    # # https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
    # nx.draw(
    #     nx_graph, pos=pos, node_size=10, linewidths=1, font_size=15, with_labels=True
    # )
    # plt.show()


def cleanwater_gis2neo4j() -> None:
    gis_to_neo4j = GisToNeo4J(srid=DEFAULT_SRID)
    neo4j_graph = gis_to_neo4j.create_network()


# TODO: Deprecated. for test purposes only.
def create_pipes_network() -> None:
    gis_to_nx = GisToNetworkX(srid=DEFAULT_SRID)
    gis_to_nx.create_network2()


def main():
    parser = argparse.ArgumentParser(description="Run Clean Water Toolkit functions")

    parser.add_argument(
        "--method", help="Convert the gis network to a connected graph network."
    )

    args = parser.parse_args()

    if args.method == "gis2nx":
        cleanwater_gis2nx()

    if args.method == "gis2neo4j":
        cleanwater_gis2neo4j()

    if args.method == "createpipes":
        create_pipes_network()


main()
