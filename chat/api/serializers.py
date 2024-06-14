from rest_framework import serializers
from ..models import Room, Message , AppMeta

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','name', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'content', 'created_at']

class AppMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppMeta
        fields = ['id', 'meta_key', 'meta_value', 'created_at']
