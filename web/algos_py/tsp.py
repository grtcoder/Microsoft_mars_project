from .astar import *
from math import *
from itertools import permutations


def tsp_solver(map, source, end_points, grid_size, allow_diagonal,
               dont_cross_corner):

    # # store all vertex apart from source vertex
    # end_points= []
    # for i in range(V):
    #     if i!= s:
    #         end_points.append(i)
    dict = {}
    end_points.append(source)
    n = len(end_points)
    for i in range(n):
        for j in range(i + 1, n):
            path_nodes, green_nodes, closed_nodes, length = astar_search(
                map, end_points[i], end_points[j], "euclidean", allow_diagonal,
                1, grid_size, "tsp", dont_cross_corner)
            path_nodes.reverse()
            dict[(end_points[i][0], end_points[i][1], end_points[j][0],
                  end_points[j][1])] = [path_nodes, length]

           
            path_nodes1, green_nodes1, closed_nodes1, length1= astar_search(
                map, end_points[j], end_points[i], "euclidean", allow_diagonal,
                1, grid_size, "tsp", dont_cross_corner)
            path_nodes1.reverse()
            dict[(end_points[j][0], end_points[j][1], end_points[i][0],
                  end_points[i][1])] = [path_nodes1, length1]

    end_points.remove(source)

    # store minimum weight Hamiltonian Cycle
    min_path = inf
    final_cnt = inf
    

    p = permutations(end_points, len(end_points))
    cnt=0
    for a_perm in p:
        
        cnt+=1
        
        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = source
        for i in range(len(a_perm)):

            # path_nodes = dict[(k[0], k[1], a_perm[i][0],
            #                    a_perm[i][1])][0]
            length = dict[(k[0], k[1], a_perm[i][0], a_perm[i][1])][1]
            #list_of_paths.append(path_nodes)
            current_pathweight += length
            k = a_perm[i]
        #current_pathweight += graph[k][s]    no return journey

        # update minimum
        if current_pathweight < min_path:
            min_path = current_pathweight
            final_cnt=cnt


    print("here")
    print(min_path)
    print(final_cnt)

    cnt1=0
    chk=0
    min_perm=[] 
    p = permutations(end_points, len(end_points))

    for a_perm in p:
       # print("inside")
        cnt1+=1
        print(cnt1)
        if cnt1==final_cnt:
            
            k=source
            #print("here")
            
            for i in range(len(a_perm)):

                path_nodes = dict[(k[0], k[1], a_perm[i][0],
                                a_perm[i][1])][0]
                #length = dict[(k[0], k[1], a_perm[i][0], a_perm[i][1])][1]
                print(path_nodes)
                min_perm.append(path_nodes)
                #current_pathweight += length
                k = a_perm[i]



            
            print("inside_tsp",min_perm)
            chk=1
            break
        if chk==1:
            break


    return min_path, min_perm


# Driver Code
# if __name__ == "__main__":

#     # matrix representation of graph
#     graph = [[0, 10, 15, 20], [10, 0, 35, 25],
#              [15, 35, 0, 30], [20, 25, 30, 0]]
#     s = 0
#     print(tsp(graph, s))
