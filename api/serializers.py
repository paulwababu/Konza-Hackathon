from rest_framework import serializers
from carwash import models
from stockmgmt import models as md
from todo import models as md2

class CarWashSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'licensePlate',
            'vehicleType',
            'created_date',
            'amountPaid',
        )
        model = models.CarWash

class StockMgmtSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'model',
            'category',
            'pieces',
            'unitPrice',
        )
        model = md.Stock        
       

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = md2.Todo
        fields = "__all__"