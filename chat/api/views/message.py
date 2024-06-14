from rest_framework.response import Response
from rest_framework import status


# chat/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message , Room
from ..serializers import MessageSerializer

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
