import sys
import logging

from Models.Graph import Graph


class LogicController:

    # MINIMIZE_GRAPH_BELLMANFORD
    # Minimizes the passed graph with the modified Bellman-Ford algorithm
    #
    # @params: Models/Graph graph
    # @return: minimized Modles/Graph object
    def minimize_graph(self, graph):
        logging.debug('Starting modified Bellman-Ford algorithm with %s nodes and %s edges...',
                      len(graph.nodes), len(graph.edges))

        # Repeat for every node in the graph
        for curr_node in graph.nodes:
            self.broadcast(graph, curr_node)

        # Create new minimized graph
        minimized_edges = []
        for node in graph.nodes:
            if node.next_hop not in minimized_edges:
                minimized_edges.append(node.next_hop)
        minimized_graph = Graph(graph.nodes, minimized_edges)

        # Print the graph and return
        self.print_graph(minimized_graph)
        return minimized_graph

    def broadcast(self, graph, curr_node):
        logging.debug("Current node (%s = %s) is broadcasting...", curr_node.name, curr_node.root_id)
        # Broadcast cost and root_id to next node of every edge of the current node
        current_edges = graph.find_edges_for_node(curr_node)
        curr_node.count += 1
        for edge in current_edges:
            # Find the node the edge points to
            if edge.frm == curr_node.name:
                next_node = graph.find_node_by_name(edge.to)
            else:
                next_node = graph.find_node_by_name(edge.frm)
            logging.debug("Sending root_id %s and cost %s to next_node (%s = %s)...",
                          curr_node.root_id, curr_node.cost, next_node.name, next_node.root_id)

            curr_cost = curr_node.cost + edge.cost

            # Update cost and root_id (only if next_node id is greater curr_node id)
            if next_node.root_id > curr_node.root_id:
                logging.debug("next_node root_id %s is larger than curr_node root id %s, updating values...",
                              next_node.root_id, curr_node.root_id)
                next_node.root_id = curr_node.root_id
                next_node.cost = curr_cost
                next_node.next_hop = edge
                logging.debug("Node %s now has root_id %s and cost %s",
                              next_node.name, next_node.root_id, next_node.cost)
                self.broadcast(graph, next_node)
            # Update cost of root node only if it is smaller than the current cost of the next node
            elif (next_node.root_id == curr_node.root_id) and (curr_cost < next_node.cost):
                logging.debug("next_node root_id %s is smaller or equal to curr_node root id %s with smaller cost, "
                              "updating...",
                              next_node.root_id, curr_node.root_id)
                next_node.cost = curr_cost
                next_node.next_hop = edge
                logging.debug("Node %s now has root_id %s and cost %s",
                              next_node.name, next_node.root_id, next_node.cost)
                self.broadcast(graph, next_node)

    # PRINT_GRAPH
    # Print a passed graph in a very pretty way
    #
    # @params: Graph graph
    # @returns: None
    @classmethod
    def print_graph(cls, graph):
        logging.info("Nodes with smallest cost to root %s:", min(graph.nodes, key=lambda x: x.node_id).name)
        print("Name\tID\tCost to Root\tNext Hop to Root\tBroadcast Count")
        nodes = ""
        for node in graph.nodes:
            if node.next_hop.cost == -1:
                next_hop = "Is Root"
            else:
                next_hop = (node.next_hop.frm + "->" + node.next_hop.to + ": " + str(node.next_hop.cost))
            nodes += (node.name + "\t" +
                      node.node_id + "\t" +
                      str(node.cost) + "\t\t" +
                      "%-15s" % next_hop + "\t\t" +
                      str(node.count) + "\n")
        print(nodes)

    # FIND_MINIMAL_COST_EDGE
    # Finds the edge with the minimal cost in an array of Models/Edge objects
    #
    # @params: Array[Models/Edge] available_edges
    # @return: Models/Edge object
    @classmethod
    def find_minimal_cost_edge(cls, edges):
        min_cost = sys.maxsize
        min_edge = None

        # Iterate through every edge in the reachable array
        for edge in edges:
            # if edge not in excluded_edges:
            # Find the minimal cost
            if edge.cost < min_cost:
                min_cost = edge.cost
                min_edge = edge

        return min_edge
