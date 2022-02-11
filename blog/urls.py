from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('edituser/', views.editUser, name="edituser"),

    path('room/<str:pk>/', views.the_room, name="room"),
    path('create/', views.createRoom, name="create"),
    path('update/<str:pk>', views.updateRoom, name="update"),
    path('delete/<str:pk>', views.deleteRoom, name="delete"),
    path('profile/<str:pk>/', views.userProfile, name="profile"),

    path('delete_message/<str:pk>', views.deleteMessage, name="delete_message"),
    path('topics', views.mobileTopics, name="topics"),
    path('activity', views.activity_mobile, name="activity"),

]
