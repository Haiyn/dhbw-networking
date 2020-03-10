import json
import os

from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node


class FileController:

    # CHECKS IF GIVEN PATH IS VALID
    @classmethod
    def is_path_valid(cls, path):
        # if path is empty, it is not a valid path
        if path is None:
            return False

        # check if the file exists and that it is accessible
        try:
            if os.path.exists(path):
                open(path, 'r')
                return True
            else:
                return False
        except OSError:
            return False
        except TypeError:
            print("[FATAL] Path is in an invalid type!")
            return False

    # DECODES A JSON INTO A GRAPH OBJECT
    @classmethod
    def json_to_graph(cls, inputpath):
        with open(inputpath, 'r') as contents:
            try:
                # Load the JSON into a dictionary
                graph_dict = json.load(contents)

                # Create arrays with node and edge object values
                node_objects = []
                edge_objects = []
                for node in graph_dict["nodes"]:
                    node_objects.append(Node(node["id"], node["name"]))
                for edge in graph_dict["edges"]:
                    edge_objects.append(Edge(edge["source"], edge["destination"], edge["weight"]))

                # Put the node and edge arrays in the Graph object and return it
                return Graph(node_objects, edge_objects)

            except json.decoder.JSONDecodeError:
                print("[FATAL] The contents of \'", inputpath, "\' are not a well formed JSON! Please see data "
                                                               "specifications in the README for more information.")
                exit(2)
        # Map the file contents to a hashmap

    # DUMPS A GRAPH OBJECT AS A JSON FILE
    @classmethod
    def graph_to_json(cls, graph, exportpath):
        print("graph to json")
