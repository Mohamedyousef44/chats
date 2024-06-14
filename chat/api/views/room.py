from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import  Room , AppMeta
from ..serializers import RoomSerializer

@api_view(['GET', 'POST'])
def rooms_view(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def single_room_view(request, id):
    try:
        room = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def room_count_view(request):
    # Try to get the room count from AppMeta
    try:
        meta = AppMeta.objects.get(meta_key='rooms_count')
        room_count = int(meta.meta_value)
    except AppMeta.DoesNotExist:
        # If not found, calculate the room count
        room_count = Room.objects.count()
        # Save the count to AppMeta
        AppMeta.objects.create(meta_key='rooms_count', meta_value=str(room_count))
    return Response({'room_count': room_count}, status=status.HTTP_200_OK)