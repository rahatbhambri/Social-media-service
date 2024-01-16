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

    user_data = Db.users.find_one({"email" : email}, {"password" : 0, "_id": 0})
    if user_data:
        return ErrorResponse(message = "User with email already exists")
    else:
        data = {"email" : email, "password" : passw}
        Db.users.insert_one(data)
        data.pop("_id")
        return SuccessResponse(message= "User created successfully", data = data)



