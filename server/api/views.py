from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
# Create your views here.
@api_view(('POST',))
def test(request):
<<<<<<< HEAD
    print(request.GET)
    return Response({})
=======
    print(request.POST)
    return Response({'a':'b'})
>>>>>>> b08d6d044c69939bcb0102000723ab0b385d8726
