import sys
import logging

from Models.Graph import Graph


class LogicController:

    # MINIMIZE_GRAPH
    # Minimizes the passed graph with prims algorithm
    #
    # @params: Models/Graph graph
    # @return: minimized Modles/Graph object
    def minimize_graph_prim(self, graph):
        # Start with the smallest node_id in the graph object

        available_edges = []
        start_node = min(graph.nodes, key=lambda x: x.node_id)
        start_node.cost = 0
        available_edges += self.find_edges_for_node(graph, start_node)
        minimized_graph = Graph([start_node], [])

        logging.debug('Starting algorithm at node %s with %s available edges', start_node.name, len(available_edges))

        logging.debug('Original graph: %s nodes, %s edges', len(graph.nodes), len(graph.edges))

        # While not all nodes are reachable yet, repeat
        while len(minimized_graph.nodes) < len(graph.nodes):
            logging.debug('Iteration: %s', len(minimized_graph.nodes))
            logging.debug('Visited nodes:')
            for node in minimized_graph.nodes:
                logging.debug(node.name)
            logging.debug('Available edges (%s):', len(available_edges))
            for edge in available_edges:
                logging.debug('%s to %s with cost %s',
                              edge.frm, edge.to, edge.cost)

            # Find the available edge with the minimal cost and add it to the minimized graph
            new_edge = self.find_minimal_cost_edge(available_edges)

            # Remove the new minimal edge from the available ones so it isn't used again
            available_edges.remove(new_edge)
            # Remove all edges in available_edges that have the same destination as the new edge
            for edge in graph.edges:
                if edge in available_edges and edge.to == new_edge.to:
                    available_edges.remove(edge)

            # Add the minimal edge to the minimized graph
            minimized_graph.edges.append(new_edge)
            logging.debug('New minimized edge: %s to %s with cost %s | Minimized edges: %s',
                          new_edge.frm, new_edge.to, new_edge.cost, len(minimized_graph.edges))

            # Find out which of the edge links (to or frm) is the new node
            if graph.find_node_by_name(new_edge.to) in minimized_graph.nodes:
                new_node_name = new_edge.frm
            else:
                new_node_name = new_edge.to

            # Find the new node that new_edge connects
            new_node = graph.find_node_by_name(new_node_name)
            if new_node not in minimized_graph.nodes:
                # Add the new node to the minimized graph
                minimized_graph.nodes.append(new_node)

            # Add the cost of the new edge to the cost of the previous node
            if new_edge.frm == new_node_name:
                new_node.cost = graph.find_node_by_name(new_edge.to).cost + new_edge.cost
            else:
                new_node.cost = graph.find_node_by_name(new_edge.frm).cost + new_edge.cost

            # Check which of the new edges of new_node connect to a node that wasn't visited yet
            for edge in self.find_edges_for_node(graph, new_node):
                # if the destination of the edge isn't visited and the edge isn't available yet, add it
                if (graph.find_node_by_name(edge.to) not in minimized_graph.nodes
                    or graph.find_node_by_name(edge.frm) not in minimized_graph.nodes) \
                        and edge not in available_edges:
                    available_edges.append(edge)
                    logging.debug('New available edge from new node: %s, %s, %s | Available edges: %s',
                                  edge.frm, edge.to, edge.cost, len(available_edges))

            # Remove all edges that go to the new_node
            for edge in available_edges:
                if edge.to == new_node.name:
                    available_edges.remove(edge)

        logging.debug('Minimized graph: %s nodes, %s edges', len(minimized_graph.nodes), len(minimized_graph.edges))

        self.print_graph(minimized_graph)
        return minimized_graph

    # PRINT_GRAPH
    # Print a passed graph in a very pretty way
    #
    # @params: Graph graph
    # @returns: None
    @classmethod
    def print_graph(cls, graph):
        logging.info("Nodes with smallest cost to root (%s):", graph.nodes[0].name)
        nodes = ""
        for node in graph.nodes:
            nodes += node.name + ": " + str(node.cost) + "\n"
        print(nodes)

        logging.info("Edges:")
        edges = ""
        for edge in graph.edges:
            edges += edge.frm + " to " + edge.to + " with cost " + str(edge.cost) + "\n"
        print(edges)

    # FIND_MINIMAL_COST_EDGE
    # Finds the edge with the minimal cost in an array of Models/Edge objects
    #
    # @params: Array[Models/Edge] available_edges
    # @return: Models/Edge object
    @classmethod
    def find_minimal_cost_edge(cls, edges):
        min_cost = sys.maxsize
        min_edge = None

        # Iterate through every edge in the reachable array
        for edge in edges:
            # if edge not in excluded_edges:
            # Find the minimal cost
            if edge.cost < min_cost:
                min_cost = edge.cost
                min_edge = edge

        return min_edge

    # FIND_EDGES_FOR_NODE
    # Finds all edges in a graph to or from a given node. Optionally, multiple nodes can be excluded via name
    #
    # @params: Graph graph, Node node, String[] excluded
    # @returns: Edge[]
    @classmethod
    def find_edges_for_node(cls, graph, node, excluded=None):
        if excluded is None:
            excluded = []

        edges = []
        for edge in graph.edges:
            if (edge.to == node.name) or (edge.frm == node.name):
                if (edge.to in excluded) or (edge.frm in excluded):
                    continue
                else:
                    edges.append(edge)

        logging.debug('Found %s edges for node %s', len(edges), node.name)
        return edges
