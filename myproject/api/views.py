from rest_framework.response import Response 
from rest_framework.decorators import api_view 
import json
import random
from myproject.settings import Db
from api.serializers import UserSerializer
from .responses import *


@api_view(['GET'])
def attemptLogin(request): 
    email = str(request.GET.get('email')).lower()
    passw = str(request.GET.get('password'))
    data = {"email" : email, "password" : passw}

    ser = UserSerializer(data = data)
    if ser.is_valid():
        user_data = Db.users.find_one(data, {"password" : 0})
        if not user_data:
            return Response({"error" : "user not found"}, status=404)
        else:
            return Response({"success": user_data})
    else:
        return Response({"error": "Invalid data"}, status=400)


@api_view(['POST'])
def signup(request):
    data = request.data
    email = str(data.get('email'))
    passw = str(data.get('password'))

    user_data = Db.users.find_one({"email" : email}, {"password" : 0})
    if user_data:
        return Response({"error" : "User with email already exists"})
    else:
        data = {"email" : email, "password" : passw}
        Db.users.insert_one(data)
        return 





# @api_view(['GET', 'POST'])
# def getSampleData(request):
#     if request.method == 'GET':
#         print(mid_p)
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(run_tasks())
#         loop.close()
        
#         return Response({"1": "Sample data "})
#     else:
#         return Response({"1": "POST data "})


# @api_view(['GET'])
# def monitorTask(request):
#     t_id = str(request.GET.get('task_id'))
#     result = AsyncResult(t_id)

#     response_data = {
#         'task_id': t_id,
#         'status': result.status,
#     }
#     return Response(response_data)


# @api_view(['POST'])
# def addItem(request):
#     serializer = ItemSerializer(data = request.data) 
#     if serializer.is_valid():
#         serializer.save() 
    
#     return Response(serializer.data)


# @api_view(['GET'])
# def getOrder(request):
#     o_id = int(request.GET.get('order_id'))
#     item = request.GET.get('item')

#     return Response({"1: Bad request"})


# @api_view(['POST'])
# def insertOrders(request):

#     # prod_ids = ["A", "B", "C", "D"]
#     # orders_to_insert = []
#     # for i in range(1000000):
#     #     order = {"order_id": i, "item": "Product" + random.choice(prod_ids), "quantity": random.randint(1, 500)}
#     #     orders_to_insert.append(order)
    
#     # if Db.Orders.insert_many(orders_to_insert):
#     #     return JsonResponse({"1": "SuccesResponse"})
#     return JsonResponse({"1" : "Error occured"})



