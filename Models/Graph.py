class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def find_node_by_id(self, needed_id):
        for node in self.nodes:
            if node.node_id == needed_id:
                return node
        return None
