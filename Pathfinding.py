# tempory class node will delete later need to import node from files
import math
import random as rand
from Node import Node
from Node import nodeDistance
from Road import Road
def reconstructPath( cameFrom, current):
    totalPath = []
    print("current id ", current.id)
    totalPath.append(current)
    while str(current.id) in cameFrom.keys():
        print( "current is", current)
        current = cameFrom[str(current.id)]
        totalPath.insert(0,current)
    return totalPath

def findLowestFval(set) -> Node:
    if len(set) == 0:
        raise ValueError("There are no Node")
    lowestNode = set[0]
    for currNode in set: 
        if currNode.fScore is not None and lowestNode.fScore > currNode.fScore:
            lowestNode = currNode
    return lowestNode


def aStar(start : Node, goal : Node):
    ##For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from the start
    ## to n currently known.
    cameFrom = {}

    ## For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = {}
    gScore[str(start.id)] = 0

    ## For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    #3 how cheap a path could be from start to finish if it goes through n.
    fScore = {}
    fScore[str(start.id)] = nodeDistance(start, goal)

    ## The set of discovered nodes that may need to be (re-)expanded.
    ## Initially, only the start node is known.
    ## This is usually implemented as a min-heap or priority queue rather than a hash-set.
    start.fScore = fScore[str(start.id)]
    openSet = []
    openSet.append(start)
    
    #while openSet is not empty
    while len(openSet) != 0:
        ## This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        ## current := the node in openSet having the lowest fScore[] value
        current = findLowestFval(openSet) 
        #print("currentid found lowest: ", current.id)
        #print("lowst recoded gScore: ", gScore[str(current.id)])
        if current == goal:
            #print("current is goal")
            return reconstructPath(cameFrom, current)
        openSet.remove(current)
        if str(current.id) not in gScore:
            gScore[str(current.id)] = nodeDistance(current, goal)
            fScore[str(current.id)] = current.fScore
        ##for each neighbor of current
        #print("CurrentId is" , current.id)
        for neighbor in current.edges:
            neighborNode = neighbor.get_other_node(current)
            ## if neighbor id is not mapped into gScore then add to gscore and fscore
            #print("currentid", current.id )
            #print("neighborNode id", neighborNode.id)
            if str(neighborNode.id) not in gScore:
                #print("neighborNode added")
                gScore[str(neighborNode.id)] = neighborNode.gScore
                fScore[str(neighborNode.id)] = neighborNode.fScore
            ## d(current,neighbor) is t1 xhe weight of the edge from current to neighbor
            ## tentative_gScore is the distance from start to the neighbor through current
            ##tentative_gScore := gScore[current] + d(current, neighbor)
            #print ("Current gScore" , gScore[str(current.id)])
            #print("neigbor id gScore",gScore[str(neighborNode.id)])  
            tentiveGScore = gScore[str(current.id)] + neighbor.edgeLength()
            #print("tentiveGScore: ", tentiveGScore)
            #print("gscore of neigbor: ", gScore[str(neighborNode.id)])
            if tentiveGScore < gScore[str(neighborNode.id)]:
                ## This path to neighbor is better than any previous one. Record it!
                cameFrom[str(neighborNode.id)] = current
                gScore[str(neighborNode.id)] = tentiveGScore 
                fScore[str(neighborNode.id)] = tentiveGScore + nodeDistance(goal, neighborNode)
                #print("Size of openSet: ", len(openSet))
                if neighborNode not in openSet:
                    #print( neighborNode.id, " Added to open set.")
                    openSet.append(neighborNode)
    ##Open set is empty but goal was never reached
    raise("not Path Found")
    return -1
    


if __name__ == "__main__":
    
    rand.seed(0)
    map = []
    testNode0 = Node(0,0,0)
    testNode1 = Node(1,4,1)
    testNode2 = Node(2,5,6)
    testNode3 = Node(3,10,11)
    testNode4 = Node(4, 9, 14)
    #create roads
    Road0 = Road(0,testNode0, testNode1)
    Road1 = Road(1,testNode1, testNode2)
    Road2 = Road(2, testNode2, testNode3)
    Road3 = Road(3, testNode4, testNode1)
    #store roads into the node edge case 
    testNode0.edges.append(Road0)
    testNode1.edges.append(Road0)
    testNode1.edges.append(Road1)
    testNode1.edges.append(Road3)
    testNode2.edges.append(Road1)
    testNode2.edges.append(Road2)
    testNode3.edges.append(Road2)
    testNode4.edges.append(Road3)
    #store into test map
    map.append(testNode0)
    map.append(testNode1)
    map.append(testNode2)
    map.append(testNode3)
    map.append(testNode4)
    #store into list 
    #print("length of map",len(map))
    testPath = aStar(testNode4, testNode3)
    print("Length of path is: ", len(testPath))
    for i in range(len(testPath)):
        print(testPath[i].id)