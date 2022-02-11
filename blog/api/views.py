from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Room
from .serializers import RoomModel


@api_view(['GET'])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/rooms",
        "GET /api/rooms/create",
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    seriliazer = RoomModel(rooms, many=True)
    return Response(seriliazer.data)


@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    seriliazer = RoomModel(rooms, many=False)
    return Response(seriliazer.data)
