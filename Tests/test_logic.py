import unittest
from Controllers.LogicController import LogicController

from Models.Edge import Edge
from Models.Graph import Graph
from Models.Node import Node

logiccontroller = LogicController()


# Naming convention for unit test methoods:
# test_Should_ExpectedBehavior_When_StateUnderTest
class LogicTest(unittest.TestCase):

    nodes = [Node(1, "A"), Node(2, "B"), Node(3, "C"), Node(4, "D")]
    edges = [Edge("A", "B", 1), Edge("A", "C", 4), Edge("A", "D", 3), Edge("B", "D", 2), Edge("C", "D", 5)]
    graph = Graph(nodes, edges)

    # MINIMIZE_GRAPH
    def test_Should_ReturnMinimalGraph_When_PassedTestGraph(self):
        # Construct the input graph and the expected graph

        expected = Graph(self.nodes, [Edge("A", "B", 1), Edge("B", "D", 2), Edge("A", "C", 4)])

        actual = logiccontroller.minimize_graph_prim(self.graph)

        # Assert that the minimized edge count is the count of all nodes - 1
        # Note: There is no
        self.assertEqual(len(actual.nodes) - 1, len(actual.edges))

        # Assert that both lists are the same (compares the elements)
        self.assertCountEqual(actual.nodes, expected.nodes)

        # Note: Asserting that all edges from expected are also in actual is not possible because python compares the
        #       instances, not if the object has the same content. So Edge("A", "B", 1) != Edge("A", "B", 1)
        #       because they might have the same content but they are not the same instance
        #       Uncomment to see this effect:
        # for edge in expected.edges:
        #    self.assertIn(edge, actual.edges)

    # FIND_MINIMAL_COST_EDGE
    def test_Should_ReturnMinimalWeightEdge_When_PassedEdgeList(self):
        expected = Edge("A", "B", 1)

        actual = logiccontroller.find_minimal_cost_edge(self.edges)

        self.assertEqual(actual.frm, expected.frm)
        self.assertEqual(actual.to, expected.to)

    # FIND_EDGES_FOR_NODE
    def test_Should_ReturnAllConnectedEdges_When_PassedGraphAndNodeA(self):
        expected = [Edge("A", "B", 1), Edge("A", "C", 4), Edge("A", "D", 3)]

        actual = logiccontroller.find_edges_for_node(self.graph, self.graph.nodes[0])

        self.assertEqual(len(expected), len(actual))


if __name__ == '__main__':
    unittest.main()
