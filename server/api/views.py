from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from api.algos_py.astar import *


# Create your views here.
@api_view(('POST',))
def test(request):
    print(request.POST['start'])
    # path_nodes, green_nodes, closed_nodes = astar_search(request.POST['grid'], request.POST['start'], request.POST['end'], request.POST['heuristic'], request.POST['allowDiagonal'], request.POST['weight'] )
    # print(path_nodes,green_nodes,closed_nodes)
    return Response({'a':'b'})
