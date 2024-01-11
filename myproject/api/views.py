from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from base.models import Item 
from .serializers import ItemSerializer
import json
from django.http import JsonResponse
import random
from api.utils import timeit



@api_view(['GET'])
def getData(request): 
    items = Item.objects.all() 
    serializer  = ItemSerializer(items, many = True)
    return Response(serializer.data)   

@api_view(['GET'])
def getSampleData(request):
    from myproject.settings import mid_p
    print(mid_p)
    return Response({"1": "Sample data "})


@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data = request.data) 
    if serializer.is_valid():
        serializer.save() 
    
    return Response(serializer.data)


@api_view(['GET'])
def getOrder(request):
    o_id = int(request.GET.get('order_id'))
    item = request.GET.get('item')

    return Response({"1: Bad request"})


@api_view(['POST'])
def insertOrders(request):

    # prod_ids = ["A", "B", "C", "D"]
    # orders_to_insert = []
    # for i in range(1000000):
    #     order = {"order_id": i, "item": "Product" + random.choice(prod_ids), "quantity": random.randint(1, 500)}
    #     orders_to_insert.append(order)
    
    # if Db.Orders.insert_many(orders_to_insert):
    #     return JsonResponse({"1": "SuccesResponse"})
    return JsonResponse({"1" : "Error occured"})



