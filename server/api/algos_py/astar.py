# This class represents a node
import math

class Node:

    # Initialize the class
    def __init__(self, position:(), parent:()):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

# Draw a grid
"""
def draw_grid(map, width, height, spacing=2, **kwargs):
    for y in range(height):
        for x in range(width):
            print('%%-%ds' % spacing % draw_tile(map, (x, y), kwargs), end='')
        print()
"""









# If diagonal movements are allowed , than use any of the following two distances

def distance_octile(node1, node2):
    D = 1
    D2 = math.sqrt(2)
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[0] - node2.position[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

def distance_chebyshev(node1, node2):
    D = 1
    D2 = 1
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[0] - node2.position[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


# Euclidean distance can be used with any number of directions allowed

def distance_euclidean(node1, node2):
    D = 1 # D is the weight of contribution of h in f
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[0] - node2.position[1])
    return D * math.sqrt(dx * dx + dy * dy)

# Manhattan distance to be used when diagonal distance not allowed

def distance_manhattan(node1, node2):
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[0] - node2.position[1])
    return dx + dy

# But we are going to use any of the heuristic function for either case 
# when diagonal is allowed and is not allowed















"""
# Draw a tile
def draw_tile(map, position, kwargs):
    
    # Get the map value
    value = map.get(position)

    # Check if we should print the path
    if 'path' in kwargs and position in kwargs['path']: value = '+'

    # Check if we should print start point
    if 'start' in kwargs and position == kwargs['start']: value = 'S'

    # Check if we should print the goal point
    if 'goal' in kwargs and position == kwargs['goal']: value = 'E'

    # Return a tile value
    return value 
"""

def is_valid(x, y, grid_size):
    if (x >= 0 and x < grid_size[1] and y >= 0 and y < grid_size[0]):
        return True
    return False




# A* search
def astar_search(map, start, end, distance_function, allowed_diagonal, weight, grid_size):
    
    # Create lists for open nodes and closed nodes
    open = []
    closed = []

    print(start)
    print(end)
    
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)

    green_nodes = []

    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:

        # Sort the open list to get the node with the lowest cost first
        open.sort()

        # Get the node with the lowest cost
        current_node = open.pop(0)

        # Add the current node to the closed list
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            #path.append(start) 
            # Return reversed path
            return path[::-1], green_nodes, closed

        # Unzip the current node position
        (x, y) = current_node.position

        # Get neighbors
        if(allowed_diagonal == True):
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x+1, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1)]
        else:
            neighbors =  [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        # Loop neighbors
        new_green_nodes = []
        for next in neighbors:

            # Get value from map

            # check if the node is inside in a grid
            if( not is_valid(next[0], next[1], grid_size)):
                continue
            map_value = map[next[0]][next[1]]

            # Check if the node is a wall
            if(map_value == 'B'):
                continue

            # Create a neighbor node
            neighbor = Node(next, current_node)

            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue

        
            if(distance_function == "chebyshev"):
                neighbor.g = distance_chebyshev(neighbor, current_node)
                neighbor.h = distance_chebyshev(neighbor, goal_node)
                neighbor.f = neighbor.g + weight * neighbor.h

            if(distance_function == "euclidean"):
                neighbor.g = distance_euclidean(neighbor, current_node)
                neighbor.h = distance_euclidean(neighbor, goal_node)
                neighbor.f = neighbor.g + weight * neighbor.h

            if(distance_function == "manhattan"):
                neighbor.g = distance_manhattan(neighbor, current_node)
                neighbor.h = distance_manhattan(neighbor, goal_node)
                neighbor.f = neighbor.g + weight * neighbor.h

            if(distance_function == "octile"):
                neighbor.g = distance_octile(neighbor, current_node)
                neighbor.h = distance_octile(neighbor, goal_node)
                neighbor.f = neighbor.g + weight * neighbor.h

            

            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                open.append(neighbor)
                new_green_nodes.append(neighbor)
        
        green_nodes.append(new_green_nodes)

    # Return None, no path is found
    return None, green_nodes, closed

# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

# The main entry point for this module
def main():

    # Get a map (grid)
    map = {}
    chars = ['c']
    start = None
    end = None
    width = 0
    height = 0

    # Open a file
    fp = open('maze2.txt', 'r')
    
    # Loop until there is no more lines
    while len(chars) > 0:

        # Get chars in a line
        chars = [str(i) for i in fp.readline().strip()]

        # Calculate the width
        width = len(chars) if width == 0 else width

        # Add chars to map
        for x in range(len(chars)):
            map[(x, height)] = chars[x]
            if(chars[x] == 'S'):



                start = (x, height)
            elif(chars[x] == 'E'):
                end = (x, height)
        
        # Increase the height of the map
        if(len(chars) > 0):
            height += 1

    # Close the file pointer
    fp.close()
    distance_function = "manhattan"
    weight = 1
    allowed_diagonal = False
    # Find the closest path from start(S) to end(E)
    path = astar_search(map, start, end, distance_function, allowed_diagonal, weight)
    print()
    print(path)
    print()
    draw_grid(map, width, height, spacing=1, path=path, start=start, goal=end)
    print()
    print('Steps to goal: {0}'.format(len(path)))
    print()
