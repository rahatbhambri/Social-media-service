from dataclasses import field
from rest_framework import serializers 
from base.models import Item 

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    class Meta:  
        db_table = "users" 


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    class Meta:  
        db_table = "users" 
