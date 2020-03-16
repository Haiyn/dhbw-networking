import heapq
import sys
import logging
import time

from Controllers.FileController import FileController
from Models.Edge import Edge
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

        available_edges = graph.nodes[0].edges
        minimized_graph = Graph([graph.nodes[0]], [])

        logging.debug('Original graph: %s nodes, %s edges', len(graph.nodes), len(graph.edges))

        # While not all nodes are reachable yet, repeat
        while len(minimized_graph.nodes) < len(graph.nodes):
            logging.debug('Iteration: %s', len(minimized_graph.nodes))
            logging.debug('Visited nodes:')
            for node in minimized_graph.nodes:
                logging.debug(node.node_id)
            logging.debug('Available edges (%s):', len(available_edges))
            for edge in available_edges:
                logging.debug('%s, %s, %s',
                              edge.source, edge.destination, edge.weight)

            # Find the available edge with the minimal weight and add it to the minimized graph
            new_edge = cls.find_minimal_weight_edge(available_edges)
            available_edges.remove(new_edge)
            for edge in graph.edges:
                if edge in available_edges and edge.destination == new_edge.destination:
                    available_edges.remove(edge)
            minimized_graph.edges.append(new_edge)
            logging.debug('New minimized edge: %s to %s with weight %s | Minimized edges: %s',
                          new_edge.source, new_edge.destination, new_edge.weight, len(minimized_graph.edges))

            new_node = graph.find_node_by_id(new_edge.destination)
            if new_node not in minimized_graph.nodes:
                minimized_graph.nodes.append(new_node)

                for edge in new_node.edges:
                    if graph.find_node_by_id(edge.destination) not in minimized_graph.nodes \
                            and edge not in available_edges:
                        available_edges.append(edge)
                        logging.debug('New available edge from new node: %s, %s, %s | Available edges: %s',
                                      edge.source, edge.destination, edge.weight, len(available_edges))

                # for node in graph.nodes:
                #     for edge in node.edges:
                #         if edge not in available_edges and edge.destination == new_node.node_id and edge not in minimized_graph.edges:
                #             if Edge(edge.destination, edge.source, edge.weight) not in available_edges:
                #                 available_edges.append(edge)
                #                 logging.debug('New available edge: %s, %s, %s | Available edges: %s',
                #                               edge.source, edge.destination, edge.weight, len(available_edges))

            for edge in available_edges:
                if edge.destination == new_node.node_id:
                    available_edges.remove(edge)

            # Append the new node with the ID from the minimal edge
            # new_node = (graph.find_node_by_id(new_edge.source)
            #             if new_edge.destination == visited_nodes[len(visited_nodes) - 1].node_id
            #             else graph.find_node_by_id(new_edge.destination))
            # visited_nodes.append(new_node)
            # for edge in new_node.edges:
            #     if edge not in available_edges and edge not in minimized_graph.edges and \
            #             graph.find_node_by_id(edge.destination) not in visited_nodes:
            #         available_edges.append(edge)
            #         logging.debug('New available edge: %s, %s, %s | Available edges: %s',
            #                       edge.source, edge.destination, edge.weight, len(available_edges))
            # for edge in graph.edges:
            #     if edge.destination == new_node.node_id and graph.find_node_by_id(edge.source) not in visited_nodes:
            #         available_edges.append(edge)
            # logging.debug('New visited node: %s | Visited: %s',
            #               new_node.node_id, len(visited_nodes))

        logging.debug('Minimized graph: %s nodes, %s edges', len(minimized_graph.nodes), len(minimized_graph.edges))
        return minimized_graph

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
            # if edge not in excluded_edges:
            # Find the minimal weight
            if edge.weight < min_weight:
                min_weight = edge.weight
                min_edge = edge

        return min_edge
