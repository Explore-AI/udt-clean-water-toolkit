import setup  # Required. Do not remove.
from cwa_geod.core import AnalysisCore


def main():
    analysis = AnalysisCore()
    # analysis.run()


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
