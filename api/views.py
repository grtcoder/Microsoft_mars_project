from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from .algos_py.astar import *
from .algos_py.jps import *
from .algos_py.ida_star import *
import json
import time


# Create your views here.
@api_view(('POST', ))
def test(request):
    start = time.process_time()
    print(request.POST)
    print(bool(json.loads(request.POST['dontCrossCorners'])))
    # print(json.loads(request.POST['end']))
    print(request.POST['selected_header'])
            

    if request.POST['selected_header']=="ida_header":
        ops=[]
        length=0
        path_nodes = iterative_deepening_a_star(
            json.loads(request.POST['grid']), json.loads(request.POST['start']),
            json.loads(request.POST['end']), request.POST['heuristic'],
            json.loads(request.POST['allowDiagonal']), bool(json.loads(request.POST['dontCrossCorners'])))

        path_nodes.reverse()
            # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': ops,
            'length': round(length, 2),
            'time': round((time.process_time() - start) * 1000, 2)
        }


    elif(request.POST['selected_header'] == "jump_point_header"):
        path_nodes, time2, green_nodes, closed_nodes, length = method(
            json.loads(request.POST['grid']), json.loads(request.POST['start']),
            json.loads(request.POST['end']), request.POST['heuristic'], request.POST['selected_header'])
        # print(len(green_nodes),len(closed_nodes))
        # print(closed_nodes)
        print(length)
        ops = []
        for i in range(len(green_nodes)):
            ops.append([closed_nodes[i], 'closed', False])
            for j in green_nodes[i]:
                ops.append([j, 'opened', False])
        ops.append([closed_nodes[-1], 'closed', False])
        path_nodes.reverse()
        # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': ops,
            'length': round(length, 2),
            'time': round(time2, 2)
        }         


    else:

        path_nodes, green_nodes, closed_nodes, length = astar_search(
            json.loads(request.POST['grid']), json.loads(request.POST['start']),
            json.loads(request.POST['end']), request.POST['heuristic'],
            json.loads(request.POST['allowDiagonal']), int(request.POST['weight']),
            json.loads(request.POST['gridsize']), request.POST['selected_header'],
            bool(json.loads(request.POST['dontCrossCorners'])))
        # print(len(green_nodes),len(closed_nodes))
        # print(closed_nodes)
        print(length)
        ops = []
        for i in range(len(green_nodes)):
            ops.append([closed_nodes[i].pos(), 'closed', False])
            for j in green_nodes[i]:
                ops.append([j.pos(), 'opened', False])
        ops.append([closed_nodes[-1].pos(), 'closed', False])
        path_nodes.reverse()
        # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': ops,
            'length': round(length, 2),
            'time': round((time.process_time() - start) * 1000, 2)
        }




      



    return Response(res)
