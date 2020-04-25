class Graph:
    def __init__(self, nodes=None, edges=None):
        if nodes is None:
            nodes = []
        if edges is None:
            edges = []
        self.nodes = nodes
        self.edges = edges

    def find_node_by_id(self, needed_id):
        """
        Finds a node in the graph by its id
        :param needed_id: Integer ID to search for
        :return: found node if found, None if not found
        """
        for node in self.nodes:
            if node.node_id == needed_id:
                return node
        return None

    def find_node_by_name(self, name):
        """
        Finds a node in the graph by its name
        :param name: String name to search for
        :return: node if found, None if not found
        """
        for node in self.nodes:
            if name == node.name:
                return node
        return None

    def find_edges_for_node(self, node):
        """
        Finds all edges that are connect to the passed node
        :param node: Node object to analyze
        :return: edges: Edge List
        """
        edges = []
        for edge in self.edges:
            if (edge.to == node.name) or (edge.frm == node.name):
                edges.append(edge)
        return edges
