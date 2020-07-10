class ida_star_solver:
    def __init__(self,l,w,start,end,allowDiag):
        self.l=l
        self.w=w
        self.start=start
        self.path=[]
        self.end=end
        self.allowDiag=allowDiag
    def idastar():
        bound=h(start)
        path.append(start)
        while(1):
            t=search(0,bound)
            if t[0]==False:
                bound=t[1]
            else:
                return (path,bound)
    def successors(node):
        ls=[]
        pos=[[0,1],[0,-1],[1,0],[-1,0]]
        pos_diag=[[1,1],[1,-1],[-1,-1],[-1,1]]
        
    def search(g,bound):
        node=path[-1]
        f=g+h(node)
        if f>bound:
            return (False,f)
        if node==end:
            return (True,f)
        
