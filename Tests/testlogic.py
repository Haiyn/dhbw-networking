import unittest
from Controllers.LogicController import LogicController

# Naming convention for unit test methoods:
# test_Should_ExpectedBehavior_When_StateUnderTest
from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node

logiccontroller = LogicController()


class LogicTest(unittest.TestCase):
    # SOLVE_GRAPH
    def test_Should_ReturnMinimalJson_When_PassedTestJson(self):
        # Required variables
        importpath = '../Resources/test.json'
        exportpath = '../Resources/export.json'
        minimalpath = '../Resources/minimal.json'

        # Solve the graph from test.json and save to export.json
        logiccontroller.solve_graph(importpath, exportpath)

        # Open the export file and read the file contents
        file = open(exportpath, 'r')
        actual = file.read()
        file.close()
        file = open(minimalpath, 'r')
        expected = file.read()
        file.close()

        self.assertEqual(expected, actual)

    # MINIMIZE_GRAPH
    def test_Should_ReturnMinimalGraph_When_PassedTestGraph(self):
        # Construct the input graph and the expected graph
        nodes = [Node(1, "A"), Node(2, "B"), Node(3, "C"), Node(4, "D")]
        edges = [Edge(1, 2, 1), Edge(1, 3, 4), Edge(1, 4, 3), Edge(2, 4, 2), Edge(3, 4, 5)]
        uminimized_graph = Graph(nodes, edges)
        expected = Graph(nodes, [Edge(1, 2, 1), Edge(1, 3, 4), Edge(2, 4, 2)])

        actual = logiccontroller.minimize_graph(uminimized_graph)

        self.assertEqual(actual, expected)

    # FIND_MINIMAL_WEIGHT_EDGE
    def test_Should_ReturnMinimalWeightEdge_When_PassedEdgeArrayWithUniqueWeights(self):
        edges = [Edge(1, 2, 1), Edge(1, 3, 4), Edge(1, 4, 3), Edge(2, 4, 2), Edge(3, 4, 5)]
        expected = Edge(1, 2, 1)

        actual = logiccontroller.find_minimal_weight_edge(edges)

        self.assertEqual(actual.source, expected.source)
        self.assertEqual(actual.destination, expected.destination)

    def test_Should_ReturnFirstMinimalWeightEdge_When_PassedEdgeArrayWithSameWeights(self):
        edges = [Edge(1, 2, 1), Edge(1, 3, 1), Edge(1, 4, 1), Edge(2, 4, 1), Edge(3, 4, 1)]
        expected = Edge(1, 2, 1)

        actual = logiccontroller.find_minimal_weight_edge(edges)

        self.assertEqual(actual.source, expected.source)
        self.assertEqual(actual.destination, expected.destination)


if __name__ == '__main__':
    unittest.main()
