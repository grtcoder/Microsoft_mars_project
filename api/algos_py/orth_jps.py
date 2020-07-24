
import math, time, heapq








class Node:

    # Initialize the class
    def __init__(self, position: [], parent: []):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

    def pos(self):
        return self.position








def distance_octile(node1, node2):
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[1] - node2.position[1])
    F = math.sqrt(2) - 1
    if dx < dy:
        return F * dx + dy
    else:
        return F * dy + dx


def distance_chebyshev(node1, node2):
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[1] - node2.position[1])
    return max(dx, dy)


# Euclidean distance can be used with any number of directions allowed


def distance_euclidean(node1, node2):
    D = 1  # D is the weight of contribution of h in f
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[1] - node2.position[1])
    return D * math.sqrt(dx * dx + dy * dy)


# Manhattan distance to be used when diagonal distance not allowed


def distance_manhattan(node1, node2):
    dx = abs(node1.position[0] - node2.position[0])
    dy = abs(node1.position[1] - node2.position[1])
    return dx + dy


# But we are going to use any of the heuristic function for either case
# when diagonal is allowed and is not allowed


def hval(node1, node2, type2, solver):
    print(type(type2))
    if solver == "breadthfirst_header" or solver == "dijkstra_header":
        return 0
    if type2 == "chebyshev":
        return distance_chebyshev(node1, node2)
    if type2 == "euclidean":
        return distance_euclidean(node1, node2)
    if type2 == "manhattan":
        return distance_manhattan(node1, node2)
    if type2 == "octile":
        return distance_octile(node1, node2)




def heuristic(a, b,type2, solver):
    a = [a[0], a[1]]
    b = [b[0], b[1]]
    print(a, b)
    node1 = Node(a, None)
    node2 = Node(b, None)
    print(node1, node2)
    print(hval(node1, node2, type2, solver))
    return hval(node1, node2, type2, solver)


    # if hchoice == 1:
    #     xdist = math.fabs(b[0] - a[0])
    #     ydist = math.fabs(b[1] - a[1])
    #     if xdist > ydist:
    #         return 14 * ydist + 10 * (xdist - ydist)
    #     else:
    #         return 14 * xdist + 10 * (ydist - xdist)
    # if hchoice == 2:
    #     return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)





def lenght(current, jumppoint, solver, grid):
    node1 = Node(current, None)
    node2 = Node(jumppoint, None)
    return gval(node1, node2, solver, grid)    



def gval(node1, node2, solver, grid):
    if solver == "breadthfirst_header":
        return node1.g + 1
    if solver == "bestfirst_header":
        return 0
    x1 = node1.position[0]
    y1 = node1.position[1]
    x2 = node2.position[0]
    y2 = node2.position[1]
    if grid[y1][x1] == "S" or grid[y1][x1] == "E":
        w1 = 1
    else:
        w1 = int(grid[y1][x1])
    if grid[y2][x2] == "S" or grid[y2][x2] == "E":
        w2 = 1
    else:
        w2 = int(grid[y2][x2])
    return node1.g + ((w1 + w2) * distance_euclidean(node1, node2)) / 2























def blocked(cX, cY, dX, dY, matrix):
    if cX + dX < 0 or cX + dX >= len(matrix):
        return True
    if cY + dY < 0 or cY + dY >= len(matrix[0]):
        return True
    if dX != 0 and dY != 0:
        #If two obstacles are present in diagonal movement
        if matrix[cX + dX][cY] == 'B' and matrix[cX][cY + dY] == 'B':
            return True
        if matrix[cX + dX][cY + dY] == 'B':
            return True
    else:
        if dX != 0:
            if matrix[cX + dX][cY] == 'B':
                return True
        else:
            if matrix[cX][cY + dY] == 'B':
                return True
    return False


def dblock(cX, cY, dX, dY, matrix):
    if matrix[cX - dX][cY] == 'B' and matrix[cX][cY - dY] == 'B':
        return True
    else:
        return False


def direction(cX, cY, pX, pY):
    dX = int(math.copysign(1, cX - pX))
    dY = int(math.copysign(1, cY - pY))
    if cX - pX == 0:
        dX = 0
    if cY - pY == 0:
        dY = 0
    return (dX, dY)


def nodeNeighbours(cX, cY, parent, matrix):
    neighbours = []
    if type(parent) != tuple:
        for i, j in [
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
        ]:
            if not blocked(cX, cY, i, j, matrix):
                neighbours.append((cX + i, cY + j))

        return neighbours

    dX, dY = direction(cX, cY, parent[0], parent[1])

    if dX == 0:
        if not blocked(cX, cY, dX, 0, matrix):
            if not blocked(cX, cY, 0, dY, matrix):
                neighbours.append((cX, cY + dY))
            if blocked(cX, cY, 1, 0, matrix):
                neighbours.append((cX + 1, cY + dY))
            if blocked(cX, cY, -1, 0, matrix):
                neighbours.append((cX - 1, cY + dY))

    else:
        if not blocked(cX, cY, dX, 0, matrix):
            if not blocked(cX, cY, dX, 0, matrix):
                neighbours.append((cX + dX, cY))
            if blocked(cX, cY, 0, 1, matrix):
                neighbours.append((cX + dX, cY + 1))
            if blocked(cX, cY, 0, -1, matrix):
                neighbours.append((cX + dX, cY - 1))
    return neighbours


def jump(cX, cY, dX, dY, matrix, goal, new_test):

    nX = cX + dX
    nY = cY + dY
    if blocked(nX, nY, 0, 0, matrix):
        return None

    if (nX, nY) == goal:
        return (nX, nY)

    oX = nX
    oY = nY

    new_test.append((oX, oY))

    
    if dX != 0:
        while True:
            if (
                not blocked(oX, nY, dX, 1, matrix)
                and blocked(oX, nY, 0, 1, matrix)
                or not blocked(oX, nY, dX, -1, matrix)
                and blocked(oX, nY, 0, -1, matrix)
            ):
                return (oX, nY)

            if (
                jump(oX, oY, 0, 1, matrix, goal, new_test) != None
                or jump(oX, oY, 0, -1, matrix, goal, new_test) != None
            ):
                return (oX, oY)

            oX += dX
            if blocked(oX, nY, 0, 0, matrix):
                return None

            if (oX, nY) == goal:
                return (oX, nY)
            new_test.append((oX, nY))
    else:
        while True:
            if (
                not blocked(nX, oY, 1, dY, matrix)
                and blocked(nX, oY, 1, 0, matrix)
                or not blocked(nX, oY, -1, dY, matrix)
                and blocked(nX, oY, -1, 0, matrix)
            ):
                return (nX, oY)

            oY += dY
            if blocked(nX, oY, 0, 0, matrix):
                return None

            if (nX, oY) == goal:
                return (nX, oY)
            new_test.append((nX, oY))

    return jump(nX, nY, dX, dY, matrix, goal, new_test)


def identifySuccessors(cX, cY, came_from, matrix, goal):
    successors = []
    neighbours = nodeNeighbours(cX, cY, came_from.get((cX, cY), 0), matrix)


    new_test = []
    for cell in neighbours:
        dX = cell[0] - cX
        dY = cell[1] - cY
        
        jumpPoint = jump(cX, cY, dX, dY, matrix, goal, new_test)
        if jumpPoint != None:
            successors.append(jumpPoint)

    return successors, new_test


def method2(matrix, start, goal, type2, solver):

    l2 = []
    for i in range(len(matrix[0])): 
        row =[] 
        for item in matrix: 
            row.append(item[i]) 
        l2.append(row) 

    matrix = l2

    start = (start[0], start[1])
    goal = (goal[0], goal[1])
     
    came_from = {}
    close_set = set()
    closed_list = []
    open_list = []
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal, type2, solver)}

    pqueue = []
    heapq.heappush(pqueue, (fscore[start], start))

    starttime = time.time()

    operations = []
    while pqueue:

        current = heapq.heappop(pqueue)[1]
        if current == goal:
            data = []
            length = gscore[current]
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data = data[::-1]
            endtime = time.time()
            #print(gscore[goal])
            return (data, round(endtime - starttime, 6), open_list, closed_list, length, operations)

        close_set.add(current)
        closed_list.append(current)
        operations.append([[current[0], current[1]], 'closed', False])
        successors, new_test = identifySuccessors(current[0], current[1], came_from, matrix, goal)
        for x in new_test:
            operations.append([[x[0], x[1]], 'tested', True])
        open_list.append(successors)
        for x in successors:
            operations.append([[x[0], x[1]], 'opened', False])
        for successor in successors:
            jumpPoint = successor

            if (
                jumpPoint in close_set
            ):  # and tentative_g_score >= gscore.get(jumpPoint,0):
                continue

            tentative_g_score = gscore[current] + lenght(current, jumpPoint, solver, matrix)

            if tentative_g_score < gscore.get(
                jumpPoint, 0
            ) or jumpPoint not in [j[1] for j in pqueue]:
                came_from[jumpPoint] = current
                gscore[jumpPoint] = tentative_g_score
                fscore[jumpPoint] = tentative_g_score + heuristic(jumpPoint, goal, type2, solver)
                heapq.heappush(pqueue, (fscore[jumpPoint], jumpPoint))
        endtime = time.time()
    return ([0], round(endtime - starttime, 6), open_list, closed_list, 0, operations)


