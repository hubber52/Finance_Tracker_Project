from rest_framework import serializers
from django.contrib.auth import get_user_model

class KafkaMessageSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=300)
    key = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)

class KafkaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model
        fields = ['uuid', 
                  'username', 
                  'email', 
                  'phone']
        read_only_fields = 'uuid'

