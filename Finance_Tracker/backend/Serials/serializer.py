from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth import authenticate

#Class to serialize user information
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ['id', 
                  'username', 
                  'password', 
                  'email', 
                  'uuid', 
                  'phone']
        extra_kwargs = {"password": {"write_only": True}}

    #Override the create function to handle password encryption properly with the 'create' method
    #When calling serializer.save()
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ['id', 
                  'username', 
                  'password', 
                  'email', 
                  'uuid', 
                  'phone']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    #Override the create function to handle password encryption properly with the 'create_user' method


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        uname = data.get('username')
        pword = data.get('password')
        if uname and pword:
            user = authenticate(username = uname, password = pword)
        else:
            raise serializers.ValidationError("Bad Credentials")
        if user and user.is_active:
            return user
        else:
            raise serializers.ValidationError("User Not Found")

    