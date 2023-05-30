from Node import nodeDistance
from Node import Node
class Road:
    def __init__(self, id, node1, node2, length, traffic=0):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.traffic = traffic  # A measure of the congestion on this road, modify as needed
        self.length = length
    #get the g score or the length between these that use this road or edge
    def edgeLength(self):
        return nodeDistance(self.node1, self.node2)
    def get_other_node(self, node):
        """Given one node that the road is connected to, return the other."""
        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            print("node is: ", node.id)
            print("other nodes are ", self.node1.id, self.node2.id)
            raise ValueError("The given node is not connected to this road.")
