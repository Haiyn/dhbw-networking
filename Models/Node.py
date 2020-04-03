from Models.Edge import Edge


class Node:
    def __init__(self, node_id, name, next_hop=Edge("NaN", "NaN", -1), cost=0, count=0):
        self.node_id = node_id
        self.root_id = node_id  # Every node assumes it is the root
        self.next_hop = next_hop  # The minimized edge
        self.name = name
        self.cost = cost
        self.count = count
