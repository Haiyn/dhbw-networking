import json
import logging
import os
from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node
import re


class FileController:
    MAX_IDENT = 2  # Maximum length of the node identifier
    MAX_ITEMS = 100  # Maximum number of imported items
    MAX_COST = 30  # Maximum edge cost value
    MAX_NODE_ID = 40  # Maximum node id value

    # IS_PATH_VALID
    # Checks if the passed path is valid
    #
    # @params: String path
    # @return: True if valid, False if invalid
    @classmethod
    def is_path_valid(cls, path):
        # if path is empty, it is not a valid path
        if path is None:
            return False

        # check if the file exists and that it is accessible
        try:
            if os.path.exists(path):
                file = open(path, 'r')  # opening with write deletes the file contents!
                file.close()
                return True
            else:
                return False
        except OSError:
            # Cannot open the file
            print('[ERROR] The path \'', path, '\' is not a valid path or the file does not exist.')
            return False
        except TypeError:
            # Path is not of type string or os.path, should never happen
            print("[FATAL] Path is in an invalid type!")
            return False

    # IMPORT_JSON_TO_GRAPH
    # Decodes a json file into a Models/Graph object
    #
    # @params: String inputpath
    # @return: Graph object
    def import_file_to_graph(self, inputpath):
        with open(inputpath, 'r') as file:
            graph = Graph()
            entries = 0
            lines = file.readlines()

            # Check if the file has the correct format:
            # Graph [name] { ... } with // comments allowed
            contents = ""
            for line in lines:
                contents += line
            # TODO: FIX THIS
            # match = re.match("(\/\/.*)*Graph .+ {[\s\S]*}", contents, re.DEBUG)
            # if match is None:
            #     logging.error("The file format is wrong! Check the import specification for the correct format.")
            #     exit(2)

            # Read the file line by line

            for line in lines:
                if entries >= self.MAX_ITEMS:
                    logging.error("File is too long! Aborting import.")
                    exit(2)

                if line.startswith('//') or line.find(';') == -1:
                    # line is a comment or not a definition
                    continue

                if line.find('-') == -1:
                    # line is a node definition
                    key = line[0: line.find('=')].strip()
                    value = line[line.find('=') + 1:line.find(';')].strip()
                    graph.nodes.append(Node(value, key))
                    logging.debug('Node definition found: %s | %s', value, key)
                elif line.find('-') != -1:
                    # line is an edge definition
                    frm = line[0: line.find('-')].strip()
                    to = line[line.find('-') + 1: line.find(':')].strip()
                    cost = line[line.find(':') + 1:line.find(';')].strip()
                    graph.edges.append(Edge(frm, to, cost))
                    logging.debug('Edge definition found: %s | %s | %s', frm, to, cost)

                entries += 1

            for node in graph.nodes:
                logging.debug('%s - %s', node.node_id, node.name)

            for edge in graph.edges:
                logging.debug('%s - %s: %s', edge.frm, edge.to, edge.cost)

            file.close()
            return graph

            # graph.matrix = [[0] * len(graph.nodes)] * len(graph.nodes)
            # for i in range(len(graph.nodes)):
            #     for j in range(len(graph.nodes)):
            #         if i == j:
            #             continue
            #
            #         for edge in graph.edges:
            #             to = graph.find_node_by_name(edge.to).node_id
            #             frm = graph.find_node_by_name(edge.frm).node_id
            #             logging.debug("%s, %s vs %s, %s", graph.nodes[i].node_id, graph.nodes[j].node_id,
            #                           graph.find_node_by_name(edge.frm).node_id, graph.find_node_by_name(edge.to).node_id)
            #             if (graph.nodes[i].node_id == to and graph.nodes[i].node_id == frm) \
            #                     or (graph.nodes[j].node_id == to and graph.nodes[i].node_id == frm):
            #                 logging.debug("Match found: %s, %s", edge.frm, edge.to)
            #                 graph.matrix[i][j] = edge.cost
            #                 break
            #
            # logging.debug('\n'.join([''.join(['{:5}'.format(item) for item in row])
            #                          for row in graph.matrix]))

    def validate_imported_data(self, graph):
        # Assert that the node names are not longer than the global setting MAX_IDENT
        # and that the node ids are not greater than the global setting MAX_NODE_ID
        for node in graph.nodes:
            if len(node.node_id) > self.MAX_IDENT:
                logging.error("Node has a name longer than MAX_IDENT (%s): '%s' with Node ID %s",
                              self.MAX_IDENT, node.name, node.node_id)
                exit(2)
            if int(node.node_id) > self.MAX_NODE_ID:
                logging.error("Node has an ID value greater than MAX_NODE_ID (%s): '%s' with Node ID %s",
                              self.MAX_NODE_ID, node.name, node.node_id)
                exit(2)

        # Assert that every edge has a source and destination that exists
        # and that the cost of every edge is not greater than the global setting MAX_COSTS
        for edge in graph.edges:
            if graph.find_node_by_name(edge.frm) is None or graph.find_node_by_name(edge.to) is None:
                logging.error("Edge references to a node that does not exist: '%s' to '%s' with cost '%s'",
                              edge.frm, edge.to, edge.cost)
                exit(2)
            if edge.cost > self.MAX_COST:
                logging.error("Edge has a cost value greater than MAX_COST: '%s' to '%s' with cost '%s'",
                              edge.frm, edge.to, edge.cost)
                exit(2)

    # EXPORT_GRAPH_TO_JSON
    # Writes a Models/Graph object to a json file
    #
    # @params: Models/Graph graph, String exportpath
    # @return: True if successful, False if invalid path or writing failed
    @classmethod
    def export_graph_to_json(cls, graph, exportpath):
        if cls.is_path_valid(exportpath):
            # Write privileges cannot be checked beforehand so possible errors need to be caught
            try:
                with open(exportpath, 'w') as file:
                    # Dump the contents of the graph object into the file
                    json.dump(graph, file, default=lambda o: o.__dict__,
                              sort_keys=False, indent=4)
                file.close()
                return True
            except IOError:
                print('[ERROR] Could not write to file', exportpath, ". Does the program have write privileges in "
                                                                     "this file?")
                return False

        else:
            print('[ERROR] The path \'', exportpath, '\' is not a valid path or the file does not exist. The file was '
                                                     'not exported.')
            return False
