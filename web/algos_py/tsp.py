
from .astar import *
from math import *
from itertools import permutations
def tsp(map, source, end_points,grid_size,allow_diagonal,dont_cross_corner): 
  
    # # store all vertex apart from source vertex 
    # end_points= [] 
    # for i in range(V): 
    #     if i!= s: 
    #         end_points.append(i) 
    dict={}
    end_points.append(source)
    n=len(end_points)
    for i in range(n):
        for j in range(i+1,n):
            path_nodes,green_nodes,closed_nodes,length=astar_search(map,end_points[i],end_points[j],"Euclidean",allowed_diagonal,1,grid_size,"tsp",dont_cross_corner)
            dict[(end_points[i],end_points[j])]= [path_nodes, length] 


    end_points.remove(source)      

  
    # store minimum weight Hamiltonian Cycle 
    min_path = inf
    final_path=[]

    p=permutations(end_points,len(end_points))
    for a_perm in p: 
        
        list_of_paths=[]
        # store current Path weight(cost) 
        current_pathweight = 0
  
        # compute current path weight 
        k = source
        for i in range(len(a_perm)): 
            
            path_nodes= dict[(k,end_points[i])][0]
            length=dict[(k,end_points[i])][1]
            list_of_paths.append(path_nodes)
            current_pathweight += length
            k = end_points[i]
        #current_pathweight += graph[k][s]    no return journey
  
        # update minimum 
        if current_pathweight<min_path:
            min_path=current_pathweight
            final_path=list_of_paths

  
    return min_path,final_path
  
  
# Driver Code 
if __name__ == "__main__": 
  
    # matrix representation of graph 
    graph = [[0, 10, 15, 20], [10, 0, 35, 25],  
             [15, 35, 0, 30], [20, 25, 30, 0]] 
    s = 0
    print(tsp(graph, s)) 