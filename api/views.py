from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import UpdateAPIView
from carwash import models
from stockmgmt import models as md
from todo import models as md2
from . import serializers
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from urllib.parse import urlparse
import json
# Create your views here.

#car wash views
class ListCarsWashed(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.CarWash.objects.all()
    serializer_class = serializers.CarWashSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['vehicleType', 'licensePlate', 'created_date']

class DetailCarsWashed(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.CarWash.objects.all()
    serializer_class = serializers.CarWashSerializer

class UpdateCarsWashedAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific todo by passing in the id of the todo to update"""
    permission_classes = (IsAuthenticated,)
    queryset = models.CarWash.objects.all()
    serializer_class = serializers.CarWashSerializer

class DeleteCarsWashedAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    permission_classes = (IsAuthenticated,)
    queryset = queryset = models.CarWash.objects.all()
    serializer_class = serializers.CarWashSerializer
########################################################################################
#stock management views
class ListStocks(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = md.Stock.objects.all()
    serializer_class = serializers.StockMgmtSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['model', 'category', 'unitPrice']

class DetailStocks(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = md.Stock.objects.all()
    serializer_class = serializers.StockMgmtSerializer


class UpdateStocksAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific todo by passing in the id of the todo to update"""
    permission_classes = (IsAuthenticated,)
    queryset = md.Stock.objects.all()
    serializer_class = serializers.StockMgmtSerializer

class DeleteStocksAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    permission_classes = (IsAuthenticated,)
    queryset = md.Stock.objects.all()
    serializer_class = serializers.StockMgmtSerializer


#######
#GET http://127.0.0.1:8000/api/v1/contacts/
# CONTACTS API VIEW
class ContactView(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        # Opening JSON file
        f = open('/home/paulsaul/Desktop/AlienX/api/contacts.json',)
        data = json.load(f)
        f.close()
        content = data
        return Response(content)


# Create your views here.
class ListTodoAPIView(ListAPIView):
    """This endpoint list all of the available todos from the database"""
    queryset = md2.Todo.objects.all()
    serializer_class = serializers.TodoSerializer

class CreateTodoAPIView(CreateAPIView):
    """This endpoint allows for creation of a todo"""
    queryset = md2.Todo.objects.all()
    serializer_class = serializers.TodoSerializer

class UpdateTodoAPIView(UpdateAPIView):
    """This endpoint allows for updating a specific todo by passing in the id of the todo to update"""
    queryset = md2.Todo.objects.all()
    serializer_class = serializers.TodoSerializer

class DeleteTodoAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    queryset = md2.Todo.objects.all()
    serializer_class = serializers.TodoSerializer