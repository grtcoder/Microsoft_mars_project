
from .astar import *

def iterative_deepening_a_star_rec(first,map,node, goal, distance, threshold,allowed_diagonal,dont_cross,path,distance_function,length,intm_path,grid_size):
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
        #path=[]
        current_node=node
        length = gval(current_node, first,"idastar_header", map)
        while current_node != first:
            path.append(current_node.position)
            current_node = current_node.parent
        path.append(first.position)
        return -distance

    estimate = distance +  hval(node, goal, distance_function,"ida_star")

    if estimate > threshold:
        #print("Breached threshold with heuristic: " + str(estimate))
        return estimate

    # ...then, for all neighboring nodes....
    min = float("inf")

    neighbors = getNeighbours(node, map, allowed_diagonal,
                                  dont_cross,grid_size)

    intm_path.append(node.position)
    for next in neighbors:
        #if map[next[1]][next[0]] != 0:
        if map[next[1]][next[0]]=='B':
            continue
        
        #intm_path.append([next[0],next[1]])
        #path.append([next[0],next[1]])
        neighbor = Node(next, node)
        
        t = iterative_deepening_a_star_rec(first,map, neighbor, goal, distance + gval(node,neighbor,"ida_star",map),
        threshold,allowed_diagonal,dont_cross,path,distance_function,length,intm_path,grid_size)
        
        if t < 0:
            # Node found
            return t
        elif t < min:
            min = t

    return min        #returning exceeding thresholds ka minimum





def iterative_deepening_a_star(map, start, goal,distance_function,allowed_diagonal,dont_cross,grid_size):
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
    goal_node = Node(goal, None)


    all_paths=[]

    
    threshold = hval(start_node, goal_node, distance_function, solver="ida_star")
    while True:
        #print("Iteration with threshold: " + str(threshold))
        path=[]
        length=0
        intm_path=[]
        first=start_node

        distance = iterative_deepening_a_star_rec(first,map, start_node, goal_node, 0, threshold,allowed_diagonal,
        dont_cross,path,distance_function,length,intm_path,grid_size)
        for pos in intm_path:
            all_paths.append([pos,'tested',True])
        intm_path.reverse()
        for pos in intm_path:
            all_paths.append([pos,'tested',False])      
                                                        #in-case of tracking recursion
        if distance == float("inf"):
            # Node not found and no more nodes to visit
            return -1
        elif distance < 0:
            # if we found the node, the function returns the negative distance
            #print("Found the node we're looking for!")
            #return -distance
            return path,all_paths,length   #final wala for yellow line
        else:
            # if it hasn't found the node, it returns the (positive) next-bigger threshold
            threshold = distance
