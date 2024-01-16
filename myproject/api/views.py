from rest_framework.response import Response 
from rest_framework.decorators import api_view , permission_classes
import json
import random
from myproject.settings import Db
from api.serializers import *
from .responses import *
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



@api_view(['GET'])
def homepage(request):
    return SuccessResponse(message="Please use /login endpoint to login") 

@api_view(['GET'])
def attemptLogin(request): 
    email = str(request.GET.get('email')).lower()
    passw = str(request.GET.get('password'))
    data = {"email" : email, "password" : passw}

    ser = UserSerializer(data = data)
    if ser.is_valid():
        user_data = Db.users.find_one(data, {"password" : 0, "_id": 0})
        if not user_data:
            #improvement
            return NotFoundResponse(message = "user with credentials could not be located", status=404)
        else:
            return SuccessResponse(data= user_data, message="Login Successfull")
    else:
        return ErrorResponse(message= "Invalid data format", status=400)


@api_view(['POST'])
def signup(request):
    data = request.data
    email = str(data.get('email'))
    passw = str(data.get('password'))
    name = str(data.get('name'))

    ser = UserSignupSerializer(data = data)
    if ser.is_valid():
        user_data = Db.users.find_one({"email" : email}, {"password" : 0, "_id": 0})
        if user_data:
            return ErrorResponse(message = "User with email already exists")
        else:
            data = {"email" : email, "password" : passw, "name" : name}
            Db.users.insert_one(data)
            data.pop("_id")
            return SuccessResponse(message= "User created successfully", data = data)
    else:
        return ErrorResponse(message="Bad Form Data")

@api_view(['PUT'])
@login_required
def reactToFriend(request):
    data = request.data
    
    user_email = str(data.get('u_email'))
    f_email = str(data.get('f_email'))
    action = data.get('action')

    if action == 'send':
        Db.users.find_one_and_update(
            {"email" : f_email}, 
            {"$push": {"incoming_requests": user_email}}
        )
        Db.users.find_one_and_update(
            {"email": user_email},
             {"$push": {"outgoing_requests": f_email}}
        )    
        return SuccessResponse(message= "Request sent successfully")
    
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
@login_required
def getFriends(request):
    u_mail = request.GET.get("user_email")
    user_data = Db.users.find_one({"email": u_mail}, {"email" : 1, "friends": 1, "_id":0})

    if user_data :
        return SuccessResponse(data = user_data)
    else:
        return NotFoundResponse(message= "user not found")


@api_view(['GET'])
@login_required
def getPendingFriends(request):
    u_mail = request.GET.get("user_email")
    user_data = Db.users.find_one({"email": u_mail}, {"email" : 1, "incoming_requests": 1, "_id":0})
    if user_data :
        if "incoming_requests" not in user_data:
            user_data["incoming_requests"] = []
        return SuccessResponse(data = user_data)
    else:
        return NotFoundResponse(message= "user not found")


@api_view(['GET'])
@login_required
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
            # n = len(users)
            # data = dict(zip( list(range(n)), users ))
            # return SuccessResponse(data = data, message= "users fetched successfully")
            return paginator.get_paginated_response(paginated_data)
        else:
            return NotFoundResponse("user not found")
