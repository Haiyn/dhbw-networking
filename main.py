import getopt
import sys
import os
import time
from Controllers.FileController import FileController
from Controllers.LogicController import LogicController


def main(argv):
    try:
        # short options accept -h, -t or custom -i [path] (i:)
        options, arguments = getopt.getopt(argv, "hti:e:", ["importpath=", "exportpath="])
    except getopt.GetoptError:
        print('[ERROR] Malformed arguments. Use -h to see help.\n')
        sys.exit(2)
    importpath = ""
    exportpath = ""
    for opt, arg in options:
        argument = arg
        if opt == '-h':
            show_help()
        elif opt == '-t':
            test_modules()
        elif opt in ("-i", "--ifile"):
            importpath = argument
        elif opt in ("-e", "--efile"):
            exportpath = argument
    # Check if import and export were selected
    if importpath and exportpath:
        solve_tree(importpath, exportpath)
    elif importpath:
        solve_tree(importpath)


# Imports a given file and solves it
def solve_tree(inputpath, exportpath=None):
    filecontroller = FileController()
    logiccontroller = LogicController()

    # Check if the paths are actual files
    if not filecontroller.is_path_valid(inputpath):
        print('[ERROR] The path \'', inputpath, '\' is not a valid path or the file does not exist.')
        exit(2)

    # import the file contents and deserialize into graph object
    print("[DEBUG] Importing data from", inputpath, "...")
    start = time.perf_counter()
    graph = filecontroller.json_to_graph(inputpath)
    end = time.perf_counter()
    print("[DEBUG] Imported data in", end - start, " s")

    # Minimize the graph object
    print("[DEBUG] Minimizing graph...")
    start = time.perf_counter()
    logiccontroller.minimize(graph)
    end = time.perf_counter()
    print("[DEBUG] Graph minimized in", end - start, "ms")

    # If an export path was given, export the resulting graph
    if exportpath is not None:
        if filecontroller.is_path_valid(exportpath):
            filecontroller.graph_to_json(graph, exportpath)
        else:
            print('[ERROR] The path \'', exportpath, '\' is not a valid path or the file does not exist. The file was '
                                                     'not exported.')


# Run all unit tests
def test_modules():
    os.system("python -m unittest")


# No Arguments given
# def default():


# Show the help information
def show_help():
    print('[INFO] Usage:\n'
          'Import a file\t\tpython main.py -i [inputfile]\n'
          'Import a file and export\tpython main.py -ie [inputfile] [exportfile]\n'
          'Run unit tests\t\tpython main.py -t\n')
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
