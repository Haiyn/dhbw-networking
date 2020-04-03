class Graph:
    def __init__(self, nodes=None, edges=None):
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []
        self.nodes = nodes
        self.edges = edges

    def find_node_by_id(self, needed_id):
        for node in self.nodes:
            if node.node_id == needed_id:
                return node
        return None

    def find_node_by_name(self, name):
        for node in self.nodes:
            if name == node.name:
                return node

    def find_edges_for_node(self, node):
        edges = []
        for edge in self.edges:
            if (edge.to == node.name) or (edge.frm == node.name):
                edges.append(edge)
        return edges
