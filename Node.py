import math
class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.edges = []  # Roads that connect to this node
        self.gScore = 500000000
        self.hScore = 500000000
        self.fScore = 500000000
        self.store = None
    #returns from current node to end node 
    #the absolute distance not from node to node 
    def setHscore(self, end):
        self.hScore = nodeDistance(self, end)
        return self.hScore
    #get distance from current node and neighbor node
    def setGscore(edgeRoad):
        return edgeRoad.edgeLength()
    
    def assign_store(self, store):
        self.store = store
        
    def assign_warehouse(self, warehouse):
        # kind of the same thing as store, I made it different for readability
        self.store = warehouse
    
#function that returns the location distance not the time it will take
def nodeDistance(fromNode, toNode) -> float:
    if isinstance(fromNode, Node) == False or isinstance(toNode, Node) == False:
        return -1
    x = toNode.x - fromNode.x
    x = abs(x**2)
    y = toNode.y - fromNode.y
    y = abs(y**2)
    return math.sqrt(x + y)