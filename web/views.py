from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from .algos_py.astar import *
from .algos_py.jps import *
from .algos_py.orth_jps import *
from .algos_py.ida_star import *
from .algos_py.tsp import *
import json
import time


# Create your views here.
def home(request):
    return render(request, 'web/home.html')


def common(request):
    return render(request, 'web/index.html')


def tsp(request):
    return render(request, 'web/TSP.html')


# Create your views here.
@api_view(('POST', ))
def tspapi(request):
    # print(request.POST)
    start = time.process_time()
    length, path_nodes = tsp_solver(
        json.loads(request.POST['grid']), json.loads(request.POST['start']),
        json.loads(request.POST['endpoints']),
        json.loads(request.POST['gridsize']),
        json.loads(request.POST['allowDiagonal']),
        bool(json.loads(request.POST['dontCrossCorners'])))
    print(path_nodes)
    path_final=[]
    for i in path_nodes:
        for j in i:
            path_final.append(j)
    print(path_final)
    res = {
        'path_nodes': path_final,
        'length': round(length, 2),
        'time': round((time.process_time() - start) * 1000, 2)
    }
    return Response(res)


@api_view(('POST', ))
def test(request):
    start = time.process_time()
    print(request.POST)
    print(bool(json.loads(request.POST['dontCrossCorners'])))
    # print(json.loads(request.POST['end']))
    print(request.POST['selected_header'])

    if request.POST['selected_header'] == "ida_header":

        path_nodes, all_nodes, length = iterative_deepening_a_star(
            json.loads(request.POST['grid']),
            json.loads(request.POST['start']),
            json.loads(request.POST['end']), request.POST['heuristic'],
            json.loads(request.POST['allowDiagonal']),
            bool(json.loads(request.POST['dontCrossCorners'])))

        #print(path_nodes)
        path_nodes.reverse()
        # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': all_nodes,
            'length': round(length, 2),
            'time': round((time.process_time() - start) * 1000, 2)
        }

    elif (request.POST['selected_header'] == "jump_point_header"):
        path_nodes, time2, green_nodes, closed_nodes, length, operations = method(
            json.loads(request.POST['grid']),
            json.loads(request.POST['start']), json.loads(request.POST['end']),
            request.POST['heuristic'], request.POST['selected_header'])
        # print(len(green_nodes),len(closed_nodes))
        # print(closed_nodes)
        print(length)

        #[[x, y], string , bool]
        print(operations)
        path_nodes.reverse()
        # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': operations,
            'length': round(length, 2),
            'time': round(time2, 2)
        }

    elif (request.POST['selected_header'] == "orth_jump_point_header"):
        path_nodes, time2, green_nodes, closed_nodes, length, operations = method2(
            json.loads(request.POST['grid']),
            json.loads(request.POST['start']), json.loads(request.POST['end']),
            request.POST['heuristic'], request.POST['selected_header'])
        # print(len(green_nodes),len(closed_nodes))
        # print(closed_nodes)
        print(length)

        #[[x, y], string , bool]
        print(operations)
        print(path_nodes)
        path_nodes.reverse()
        # print(path_nodes)
        res = {
            'path_nodes': path_nodes,
            'ops': operations,
            'length': round(length, 2),
            'time': round(time2, 2)
        }

    else:

        path_nodes, green_nodes, closed_nodes, length = astar_search(
            json.loads(request.POST['grid']),
            json.loads(request.POST['start']),
            json.loads(request.POST['end']), request.POST['heuristic'],
            json.loads(request.POST['allowDiagonal']),
            int(request.POST['weight']), json.loads(request.POST['gridsize']),
            request.POST['selected_header'],
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
