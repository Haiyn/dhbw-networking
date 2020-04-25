import argparse
import logging
import time

from Controllers.FileController import FileController
from Controllers.LogicController import LogicController


def main():
    # Argument parser that handles the cli arguments
    parser = argparse.ArgumentParser(
        description='A program to minimize spanning trees.'
    )

    # Each argument is handled differently
    parser.add_argument("-v", "--verbose",
                        help="Show info messages while running",
                        action="store_const",
                        dest="loglevel",
                        const=logging.INFO)
    parser.add_argument("-d", "--debug",
                        help="Show detailed debug messages while running",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG)
    parser.add_argument("-i", "--import",
                        help="Import a graph from a file",
                        action="store",
                        dest="importpath",
                        required=True)
    parser.add_argument("-e", "--export",
                        help="Export a graph to a file",
                        action="store",
                        dest="exportpath")

    # Parse all passed arguments
    args = parser.parse_args()

    # Handle the log level
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=args.loglevel)
    if args.loglevel == logging.DEBUG:
        logging.warning("Running in debug mode! Console outputs may be large.")

    # Handle the import and export arguments
    if args.importpath:
        if args.exportpath:
            solve_graph(args.importpath, args.exportpath)
        else:
            solve_graph(args.importpath)


def solve_graph(importpath, exportpath=None):
    """
    Controls the main function of importing and solving the graph
    :param importpath: path to file to import
    :param exportpath: path to file to export, can be None if not given as parameter in console
    """
    filecontroller = FileController()
    logiccontroller = LogicController()

    # If importpath is not valid, exit
    if not filecontroller.is_path_valid(importpath):
        exit(2)

    # Deserialize file contents into Models/Graph object
    logging.info('Importing data from %s...', importpath)
    start = time.perf_counter()
    graph = filecontroller.import_file_to_graph(importpath)
    end = time.perf_counter()
    logging.info('Imported %s Nodes, %s Edges in %.3f ms.', len(graph.nodes), len(graph.edges), (end - start) * 1000)

    # Validate the imported data
    logging.info('Validating imported data...')
    start = time.perf_counter()
    filecontroller.validate_imported_data(graph)
    end = time.perf_counter()
    logging.info('Validated data in %.3f ms.', (end - start) * 1000)

    # Minimize the graph object
    logging.info('Minimizing graph...')
    start = time.perf_counter()
    result = logiccontroller.minimize_graph(graph)
    end = time.perf_counter()
    logging.info('Graph minimized in %.3f ms.', (end - start) * 1000)

    # If an export path was given, export the resulting graph
    if exportpath is not None:
        logging.info('Exporting graph to %s...', exportpath)
        if filecontroller.export_result_to_file(result, exportpath):
            logging.info('Successfully exported graph to %s', exportpath)
        else:
            exit(2)


if __name__ == '__main__':
    main()
