import json
import os
from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node


class FileController:

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
    @classmethod
    def import_json_to_graph(cls, inputpath):
        with open(inputpath, 'r') as contents:
            try:
                # Load the JSON into a dictionary
                graph_dict = json.load(contents)

                # Create arrays with node and edge object values
                node_objects = []
                edge_objects = []

                for edge in graph_dict["edges"]:
                    edge_objects.append(Edge(edge["source"], edge["destination"], edge["weight"]))
                for node in graph_dict["nodes"]:
                    new_node = Node(node["node_id"], node["name"], [])

                    for edge in edge_objects:
                        if edge.source == new_node.node_id:
                            new_node.add_edge(Edge(edge.source, edge.destination, edge.weight))
                        elif edge.destination == new_node.node_id:
                            new_node.add_edge(Edge(edge.destination, edge.source, edge.weight))

                    node_objects.append(new_node)

                # Put the node and edge arrays in the Graph object and return it
                return Graph(node_objects, edge_objects)

            except json.decoder.JSONDecodeError:
                # Decoder could not decode the file contents
                print("[ERROR] The contents of \'", inputpath, "\' are not a well formed JSON! Please see data "
                                                               "specifications in the README for more information.")
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
