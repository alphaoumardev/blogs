from rest_framework.serializers import ModelSerializer

from blog.models import Room


class RoomModel(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
