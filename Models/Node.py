class Node:
    def __init__(self, node_id, name, edges=None):
        self.node_id = node_id
        self.name = name
        self.edges = edges

    def add_edge(self, edge):
        self.edges.append(edge)
