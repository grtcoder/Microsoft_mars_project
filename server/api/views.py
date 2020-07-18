from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from .algos_py.astar import *
import json


# Create your views here.
@api_view(('POST',))
def test(request):
    # print(json.loads(request.POST['grid']))
    # print(json.loads(request.POST['end']))
    path_nodes, green_nodes, closed_nodes = astar_search(json.loads(request.POST['grid']), json.loads(request.POST['start']), json.loads(request.POST['end']), request.POST['heuristic'], json.loads(request.POST['allowDiagonal']), json.loads(request.POST['weight']), json.loads(request.POST['gridsize']) )
    print(len(green_nodes),len(closed_nodes))
    ops=[]
    for i in range(len(green_nodes)):
        ops.append([closed_nodes[i].pos(),'closed',False])
        for j in green_nodes[i]:
            ops.append([j.pos(),'opened',False])
    ops.append([closed_nodes[-1].pos(),'closed',False])
    path_nodes.reverse()
    print(path_nodes)
    res={'path_nodes':path_nodes,'ops':ops}
    return Response(res)
