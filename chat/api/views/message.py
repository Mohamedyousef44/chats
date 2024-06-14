from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message , Room
from ..serializers import MessageSerializer
from django.core.cache import cache
import hashlib
import json

@api_view(['GET', 'POST'])
def message_view(request, id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            "room": id,
            "content": request.data['content']
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def single_message_view(request, room_id, id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        message = Message.objects.get(id=id, room=room)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = {
            "room": room_id,
            "content": request.data["content"]
        }
        serializer = MessageSerializer(message, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def search_message_view(request, id):
    search_query = request.query_params.get('message', '')

    if not search_query:
        return Response({"error": "Message query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a cache key based on the room id and search query
    cache_key = f"room_{id}_search_{hashlib.md5(search_query.encode('utf-8')).hexdigest()}"

    # Try to get the cached result
    cached_result = cache.get(cache_key)

    if cached_result:
        return Response(json.loads(cached_result), status=status.HTTP_200_OK)

    # If not cached, perform the search
    messages = Message.objects.filter(room_id=id, content__icontains=search_query)

    if not messages.exists():
        return Response({"message": "No messages found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(messages, many=True)
    response_data = serializer.data

    # Cache the result
    cache.set(cache_key, json.dumps(response_data), timeout=60*60*12)

    return Response(response_data, status=status.HTTP_200_OK)