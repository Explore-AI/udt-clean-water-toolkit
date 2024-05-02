import networkit as nk

class Neo4j2Networkit:
    def __init__(self):
        self.G = nk.Graph(edgesIndexed=True)
        self.edgelabel = self.G.attachEdgeAttribute("label", str)
        self.edgegid = self.G.attachEdgeAttribute("gid", str)
        self.nodelabel = self.G.attachNodeAttribute("label", str)
        self.values_to_drop = ['PointAsset', 'PointNode']
    
    def add_pipe(self, start_node_id, end_node_id):
        self.G.addEdge(start_node_id, end_node_id, addMissing=True)


    def process_batch(self, batch_result):
        for i in batch_result:
            start = i[1]._start_node
            x, y = start['x_coord'], start['y_coord']
            start_node_id = start._id
            start_node_label = [x for x in list(start.labels) if i not in self.values_to_drop][0]
        
            end = i[1]._end_node
            x, y = end['x_coord'], end['y_coord']
            end_node_id = end._id
            end_node_label = [x for x in list(end.labels) if i not in self.values_to_drop][0]
        
            edge_id = i[1]._id
            edge_label = i[1].type
            edge_gid = str(i[1]['gid'])    
            
            self.add_pipe(start_node_id, end_node_id)
    
            self.edgelabel[start_node_id, end_node_id] = edge_label
            self.edgegid[start_node_id, end_node_id] = edge_gid
            self.nodelabel[start_node_id] = start_node_label
            self.nodelabel[end_node_id] = end_node_label