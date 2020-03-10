def graph():
    class Graph:
        def __init__(self, nodes, edges):
            self.nodes = nodes
            self.edges = edges

    class Edge:
        def __init__(self, source, destination, weight):
            self.source = source
            self.destination = destination
            self.weight = weight

    class Node:
        def __init__(self, name, edges):
            self.name = name
            self.edges = edges
