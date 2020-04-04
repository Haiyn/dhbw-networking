class Graph:
    def __init__(self, nodes=None, edges=None):
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []
        self.nodes = nodes
        self.edges = edges

    # Finds a node in the graph by its id
    # @param Integer
    # @return Node
    def find_node_by_id(self, needed_id):
        for node in self.nodes:
            if node.node_id == needed_id:
                return node
        return None

    # Finds a node in the graph by its name
    # @param String
    # @return Node
    def find_node_by_name(self, name):
        for node in self.nodes:
            if name == node.name:
                return node

    # Finds all edges that are connect to the passed node
    # @param Node
    # @return Edges List
    def find_edges_for_node(self, node):
        edges = []
        for edge in self.edges:
            if (edge.to == node.name) or (edge.frm == node.name):
                edges.append(edge)
        return edges
