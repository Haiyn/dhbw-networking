import sys
import logging
import time

from Controllers.FileController import FileController
from Models.Graph import Graph


class LogicController:

    # SOLVE_GRAPH
    # Imports a given file and solves it
    #
    # @params: String importpath, String exportpath
    # @return: None
    @classmethod
    def solve_graph(cls, importpath, exportpath=None):
        filecontroller = FileController()

        # If importpath is not valid, exit
        if not filecontroller.is_path_valid(importpath):
            exit(2)

        # Deserialize file contents into Models/Graph object
        logging.info('Importing data from %s...', importpath)
        graph = filecontroller.import_json_to_graph(importpath)
        logging.info('Imported %s Nodes and %s Edges', len(graph.nodes), len(graph.edges))

        # Minimize the graph object
        logging.info('Minimizing graph...')
        start = time.perf_counter()
        minimized_graph = cls.minimize_graph(graph)
        end = time.perf_counter()
        logging.info('Graph minimized in %s ms', (end - start) * 1000)

        # If an export path was given, export the resulting graph
        if exportpath is not None:
            logging.info('Exporting graph to %s...', exportpath)
            if filecontroller.export_graph_to_json(minimized_graph, exportpath):
                logging.info('Successfully exported graph to %s', exportpath)
            else:
                exit(2)

    # MINIMIZE_GRAPH
    # Minimizes the passed graph with prims algorithm
    #
    # @params: Models/Graph graph
    # @return: minimized Modles/Graph object
    @classmethod
    def minimize_graph(cls, graph):
        # Start with the first node in the graph object
        reachable_nodes = [graph.nodes[0]]
        current_index = 0
        available_edges = []
        minimal_edges = []

        # While not all nodes are reachable yet, repeat
        while len(reachable_nodes) < len(graph.nodes):
            logging.debug('Iteration: %s', len(reachable_nodes))
            # Add all edges that are connected to a node that is currently reachable
            for edge in graph.edges:
                # If the current node is the source of an edge, add that edge and the destination node of the edge
                if reachable_nodes[current_index].node_id == edge.source or \
                        reachable_nodes[current_index].node_id == edge.destination:
                    available_edges.append(edge)

            new_edge = cls.find_minimal_weight_edge(available_edges)
            minimal_edges.append(new_edge)
            available_edges.remove(new_edge)
            logging.debug('New minimized edge: %s to %s with weight %s',
                          new_edge.source, new_edge.destination, new_edge.weight)

            # Append the new node with the ID from the minimal edge
            new_node = (graph.find_node_by_id(new_edge.source)
                        if new_edge.destination == reachable_nodes[current_index].node_id
                        else graph.find_node_by_id(new_edge.destination))
            reachable_nodes.append(new_node)

        return Graph(graph.nodes, minimal_edges)

    # FIND_MINIMAL_WEIGHT_EDGE
    # Finds the edge with the minimal weight in an array of Models/Edge objects
    #
    # @params: Array[Models/Edge] available_edges
    # @return: Models/Edge object
    @classmethod
    def find_minimal_weight_edge(cls, available_edges):
        min_weight = sys.maxsize
        min_edge = None

        # Iterate through every edge in the reachable array
        for edge in available_edges:
            # Find the minimal weight
            if edge.weight < min_weight:
                min_weight = edge.weight
                min_edge = edge

        return min_edge
