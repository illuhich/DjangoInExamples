from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message

# User serializer
class UserSerializer(serializers.ModelsSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

# Message serializer
class MessageSerializer(serializers.ModelsSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    reciever = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'reciever', 'message', 'timestamp']
