from django.urls import path

from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('room/', views.getRooms, name="rooms"),
    path('room/<str:pk>', views.getRoom, name="room"),
]
