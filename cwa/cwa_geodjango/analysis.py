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
    gis_to_neo4j = GisToNeo4J(srid=DEFAULT_SRID, step=250)
    neo4j_graph = gis_to_neo4j.create_network()


def cleanwater_gis2neo4j_p() -> None:
    gis_to_neo4j = GisToNeo4J(srid=DEFAULT_SRID, step=250)
    neo4j_graph = gis_to_neo4j.create_network_parallel()


# TODO: Deprecated. for test purposes only.
def create_pipes_network() -> None:
    gis_to_nx = GisToNetworkX(srid=DEFAULT_SRID)
    gis_to_nx.create_network2()


def main():
    methods_map = {"gis2neo4j": cleanwater_gis2neo4j}
    import pdb

    pdb.set_trace()


# if args.method == "gis2nx":
#     cleanwater_gis2nx()


# if args.method == "gis2neo4j":
#     cleanwater_gis2neo4j()

# if args.method == "gis2neo4jp":
#     cleanwater_gis2neo4j_p()

# if args.method == "createpipes":
#     create_pipes_network()


if __name__ == "__main__":
    main()


# from multiprocessing.pool import ThreadPool
# from multiprocessing import Pool
# from cwa_geod.assets.models import *
# from django.db import connections


# def qs_check(qs):
#     new_connection = connections.create_connection("default")
#     x = list(qs)
#     new_connection.close()
#     return x


# def run():
#     qs = TrunkMain.objects.all()
#     slices = [
#         qs[:100],
#         qs[100:200],
#         qs[200:300],
#         qs[300:400],
#     ]
#     print("a")
#     connections.close_all()
#     with ThreadPool(4) as pool:
#         xlist = pool.map(qs_check, slices)

#     qslist = []
#     for x in xlist:
#         qslist += x
#     import pdb

#     pdb.set_trace()

# procs = []
# for data in slices:
#     print(name)
#     proc = mp.Process(target=qs_check, args=(data))
#     procs.append(proc)
#     proc.start()

# for proc in procs:
#     proc.join()


# run()
