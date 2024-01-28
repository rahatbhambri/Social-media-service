from rest_framework.response import Response 
from rest_framework.decorators import api_view , permission_classes
import random, requests
from myproject.settings import Db
from api.serializers import *
from .responses import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from datetime import datetime as dt
from rest_framework_simplejwt.tokens import AccessToken
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from myproject.settings import redis
from myproject.tasks import delayed_sum, accumulate_message
from celery.result import AsyncResult
from .utils import *







@api_view(['GET'])
def homepage(request):
    result = delayed_sum.delay(5, 8)
    return SuccessResponse(data = {"taskid ": result.id}, message="Please use /login endpoint to login") 

@api_view(['GET'])
def get_result(request):
    # Retrieve the result for the given task ID
    task_id = str(request.GET.get("task_id"))
    result = AsyncResult(task_id)
    print(result.state)

    if result.ready():
        print(result.result, type(result.result))
        # Task is completed, return the result
        return SuccessResponse(data = {'status': 'Task completed', 'result': result.result})
    else:
        # Task is still processing
        return ErrorResponse(message= 'Task still processing')

@api_view(['GET'])
def attemptLogin(request): 
    email = str(request.GET.get('email')).lower()
    passw = str(request.GET.get('password'))
    data = {"email" : email, "password" : passw}


    ser = UserSerializer(data = data)
    if ser.is_valid():
        user_data = Db.users.find_one(data, {"password" : 0, "_id": 0})
        if not user_data:
            return NotFoundResponse(message = "user with credentials could not be located", status=404) 
        else:
            base_url = 'http://localhost:8000'  
            endpoint = '/token'  
            url = f'{base_url}{endpoint}'
            payload = {"username": email, "password": passw}
            response = requests.post(url, json=payload)
            response = response.json()
            #print(response)
            user_data["token"] = response.get("access")
            
            return SuccessResponse(data= user_data, message="Login Successfull")
    else:
        return ErrorResponse(message= "Invalid data format", status=400)


#signup api
@api_view(['POST'])
def signup(request):
    data = request.data
    
    email = str(data.get("email"))
    passw = str(data.get('password'))
    name = str(data.get('name'))

    ser = UserSignupSerializer(data = data)
    if ser.is_valid():
        user_data = Db.users.find_one({"email" : email}, {"password" : 0, "_id": 0})
        dup = User.objects.filter(email=email).exists()
        if user_data or dup:
            return ErrorResponse(message = "User with email already exists")
        else:
            data = {"email" : email, "password" : passw, "name" : name}
            new_user = User.objects.create_user(username=email, password=passw, email=email)
            new_user.save()

            Db.users.insert_one(data)
            data.pop("_id")

            return SuccessResponse(message= "User created successfully. use /login to signin ", data = data)
    else:
        return ErrorResponse(message="Bad Form Data")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@ratelimit(key='user', rate='3/m', method='PUT', block=True)
def reactToFriend(request):
    data = request.data
    
    try:
        email = str(request.user.username)
        print(email)
    except Exception as e:
        # Handle token decoding errors
        print(f"Error decoding token: {e}")
    
    user_email = email
    f_email = str(data.get('f_email'))
    action = data.get('action')

    if action == 'send':
        u_data = Db.users.find_one({"email": user_email},{"_id" : 0})
        #print(u_data, user_email)
        outg = u_data.get("outgoing_requests", [])
        u_fr = u_data.get("friends", [])

        if f_email not in outg and f_email not in u_fr:
            Db.users.find_one_and_update(
                {"email" : f_email}, 
                {"$push": {"incoming_requests": user_email}}
            )
            Db.users.find_one_and_update(
                {"email": user_email},
                {"$push": {"outgoing_requests": f_email}}
            )    
            return SuccessResponse(message= "Request sent successfully")
        else:
            return ErrorResponse(message="Duplicate request")
    elif action == 'accept':
        Db.users.find_one_and_update(
            {"email" : user_email}, 
            {
                "$pull": {"incoming_requests": f_email},
                "$push" : {"friends" : f_email}
            }
        )
        Db.users.find_one_and_update(
            {"email": f_email},
            {
                "$pull": {"outgoing_requests": user_email},
                "$push": {"friends" : user_email}
            }
        )
        return SuccessResponse(message= "Request Accepted successfully")
    
    elif action == 'reject':
        print(user_email, f_email)
        Db.users.find_one_and_update(
            {"email" : user_email}, 
            {"$pull": {"incoming_requests": f_email}}
        )
        Db.users.find_one_and_update(
            {"email": f_email},
            {"$pull": {"outgoing_requests": user_email}}
        )                
        return SuccessResponse(message= "Request rejected successfully")
    
    return ErrorResponse(message= "Bad Request format")



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFriends(request):
   
    try:
        email = str(request.user.username)
        print(email)
    except Exception as e:
        # Handle token decoding errors
        print(f"Error decoding token: {e}")
    
    u_mail = email
    user_data = Db.users.find_one({"email": u_mail}, {"email" : 1, "friends": 1, "_id":0})

    if user_data :
        user_data["friends"] = user_data.get("friends", [])
        return SuccessResponse(data = user_data)
    else:
        return NotFoundResponse(message= "user not found")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPendingFriends(request):
    try:
        email = str(request.user.username)
        print(email)
    except Exception as e:
        # Handle token decoding errors
        print(f"Error decoding token: {e}")
    
    u_mail = email
    
    user_data = Db.users.find_one({"email": u_mail}, {"email" : 1, "incoming_requests": 1, "_id":0})
    if user_data :
        if "incoming_requests" not in user_data:
            user_data["incoming_requests"] = []
        return SuccessResponse(data = user_data)
    else:
        return NotFoundResponse(message= "user not found")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    keyw = str(request.GET.get("keyword"))

    if "@" in keyw:
        user_data = Db.users.find_one({"email": keyw}, {"_id":0})
        if user_data :
            return SuccessResponse(data = user_data)
        else:
            return NotFoundResponse(message= "user not found")
    else:
        query = {"name": {"$regex": keyw, "$options": "i"}}
        users = list(Db.users.find(query, {"_id": 0}))
        
        paginator = PageNumberPagination()
        paginated_data = paginator.paginate_queryset(users, request)
        if users:
            return paginator.get_paginated_response(paginated_data)
        else:
            return NotFoundResponse("user not found")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#convert to ws later 
def sendMessage(request):

    email = str(request.user.username)
    data = request.data
    message = str(data.get("message"))
    f_email = str(data.get("f_email"))

    print(email, data)

    #if friend is online then send to redis channel
    #redis.hmset('user_data', {"email": email, "message": message})  
    
    #else add to unread
    Db.users.update_one({"email" : f_email}, {"$addToSet" : {"unread" : email}})
    accumulate_message(from_em = email, to_em = f_email, message= message)

    return SuccessResponse(message="message set successfully")


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def sendMessage(request):

#     email = str(request.user.username)

