from dataclasses import field
from rest_framework import serializers 
from base.models import Item 

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
        