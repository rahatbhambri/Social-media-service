from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from base.models import Item 
from .serializers import ItemSerializer
import json
from django.http import JsonResponse
import random
from api.utils import timeit
from myproject.settings import mid_p
from myproject.tasks import delayed_sum
from myproject.async_tasks import run_tasks
from celery.result import AsyncResult
import asyncio



@api_view(['GET'])
def getData(request): 
    items = Item.objects.all() 
    serializer  = ItemSerializer(items, many = True)
    return Response(serializer.data)   

@api_view(['GET', 'POST'])
def getSampleData(request):
    if request.method == 'GET':
        print(mid_p)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_tasks())
        loop.close()
        
        return Response({"1": "Sample data "})
    else:
        return Response({"1": "POST data "})


@api_view(['GET'])
def monitorTask(request):
    t_id = str(request.GET.get('task_id'))
    result = AsyncResult(t_id)

    response_data = {
        'task_id': t_id,
        'status': result.status,
    }
    return Response(response_data)


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



