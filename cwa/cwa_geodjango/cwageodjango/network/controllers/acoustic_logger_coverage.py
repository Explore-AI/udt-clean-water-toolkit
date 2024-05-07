from cwageodjango.network.models import *

class AcousticLoggerCoverage():
    def print_nodes(self):
        all_nodes = PointNode.nodes.filter(acoustic_logger='True')
        print(all_nodes)
