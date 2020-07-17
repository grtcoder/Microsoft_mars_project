from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from api.algos_py.astar import *
import json


# Create your views here.
@api_view(('POST',))
def test(request):
    print(json.loads(request.POST['grid']))
    print(json.loads(request.POST['end']))
    path_nodes, green_nodes, closed_nodes = astar_search(json.loads(request.POST['grid']), json.loads(request.POST['start']), json.loads(request.POST['end']), request.POST['heuristic'], json.loads(request.POST['allowDiagonal']), json.loads(request.POST['weight']), json.loads(request.POST['gridsize']) )
    # print(path_nodes,green_nodes,closed_nodes)
<<<<<<< HEAD
    print(path_nodes)
=======
    print(request.POST)
>>>>>>> 5a4b7c0507e8ab9a4b6c10204dc5718c1770637b
    return Response({'a':'b'})
