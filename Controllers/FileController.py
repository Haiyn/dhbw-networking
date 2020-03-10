import json
import os


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
                open(path, 'w')
                return True
            else:
                return False
        except OSError:
            return False
        except TypeError:
            print("[FATAL] Path is in an invalid type!")
            return False

    @classmethod
    def json_to_graph(cls, inputpath):
        with open(inputpath, 'r') as contents:
            try:
                content_dict = json.load(contents)
            except json.decoder.JSONDecodeError:
                print("[FATAL] The contents of \'", inputpath, "\' are not a well formed JSON!")
                exit(2)

        for entry in content_dict:
            print(entry)
        print("json to graph")
        # Map the file contents to a hashmap

    @classmethod
    def graph_to_json(cls, graph, exportpath):
        print("graph to json")
