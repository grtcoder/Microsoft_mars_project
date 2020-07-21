
from .astar import *

def iterative_deepening_a_star_rec(map,node, goal, distance, threshold,allowed_diagonal,dont_cross,path):
    """
    Performs DFS up to a depth where a threshold is reached (as opposed to interative-deepening DFS which stops at a fixed depth).
    Can be modified to handle graphs by keeping track of already visited nodes.
    :param tree:      An adjacency-matrix-representation of the tree where (x,y) is the weight of the edge or 0 if there is no edge.
    :param heuristic: An estimation of distance from node x to y that is guaranteed to be lower than the actual distance. E.g. straight-line distance.
    :param node:      The node to continue from.
    :param goal:      The node we're searching for.
    :param distance:  Distance from start node to current node.
    :param threshold: Until which distance to search in this iteration.
    :return: number shortest distance to the goal node. Can be easily modified to return the path.
     """
    #print("Visiting Node " + str(node))

    if node == goal:
        # We have found the goal node we we're searching for
        return -distance

    estimate = distance +  hval(node, goal, distance_function, solver="ida_star")

    if estimate > threshold:
        print("Breached threshold with heuristic: " + str(estimate))
        return estimate

    # ...then, for all neighboring nodes....
    min = float("inf")

    neighbors = getNeighbours(node, map, allowed_diagonal,
                                  dontcross)


    for next in neighbors:
        #if map[next[1]][next[0]] != 0:
        t = iterative_deepening_a_star_rec(map, next, goal, distance + gval(node,next,solver="ida_star",map),path)
        path.append(next)
        if t < 0:
            # Node found
            return t
        elif t < min:
            min = t

    return min        #returning exceeding thresholds ka minimum





def iterative_deepening_a_star(map, start, goal,distance_function,allowed_diagonal,dont_cross):
    """
    Performs the iterative deepening A Star (A*) algorithm to find the shortest path from a start to a target node.
    Can be modified to handle graphs by keeping track of already visited nodes.
    :param tree:      An adjacency-matrix-representation of the tree where (x,y) is the weight of the edge or 0 if there is no edge.
    :param heuristic: An estimation of distance from node x to y that is guaranteed to be lower than the actual distance. E.g. straight-line distance.
    :param start:      The node to start from.
    :param goal:      The node we're searching for.
    :return: number shortest distance to the goal node. Can be easily modified to return the path.
    """

     # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)


    all_paths=[]


    threshold = hval(start_node, goal_node, distance_function, solver="ida_star")
    while True:
        #print("Iteration with threshold: " + str(threshold))
        path=[]
        path.append(start_node)
        distance = iterative_deepening_a_star_rec(map, start_node, goal_node, 0, threshold,allowed_diagonal,dont_cross,path)
        all_paths.append(path)      #in-case of tracking recursion
        if distance == float("inf"):
            # Node not found and no more nodes to visit
            return -1
        elif distance < 0:
            # if we found the node, the function returns the negative distance
            print("Found the node we're looking for!")
            #return -distance
            return path     #final wala for yellow line
        else:
            # if it hasn't found the node, it returns the (positive) next-bigger threshold
            threshold = distance
