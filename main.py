import argparse
import logging
import os

from Controllers.LogicController import LogicController

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
parser.add_argument("-t", "--test",
                    help="Run all unit tests for this project",
                    action="store_true")
parser.add_argument("-i", "--import",
                    help="Import a graph from a json file",
                    action="store",
                    dest="importpath")
parser.add_argument("-e", "--export",
                    help="Export a graph to a json file",
                    action="store",
                    dest="exportpath")

# Parse all passed arguments
args = parser.parse_args()

# Handle the log level
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=args.loglevel)
if args.loglevel == logging.DEBUG:
    logging.warning("Running in debug mode! Console outputs may be large.")

# Start the unit tests
if args.test:
    os.system("python -m unittest discover -s")

# Handle the import and export arguments
if args.importpath:
    if args.exportpath:
        LogicController.solve_graph(args.importpath, args.exportpath)
    else:
        LogicController.solve_graph(args.importpath)

# Assure that import was passed if export was passed
if args.exportpath:
    if not args.importpath:
        logging.error("--export requires --import! See -h for help.")
