from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from blog.models import Room, Topic, Message, User
from blog.form import RoomForm, UserFrom, CustomUser
from django.db.models import Q


# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "The user does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "The username or password does not exist")
    context = {"page": page}
    return render(request, 'blog/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = CustomUser()
    if request.method == "POST":
        form = CustomUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured")
    return render(request, 'blog/login.html', {"form": form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:7]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(request, "blog/home.html", context)


def the_room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'blog/room.html', context)


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # rooms = Room.objects.get(id=pk)
    rooms = user.room_set.all()
    # rooms = Room.objects.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "rooms": rooms, "topics": topics, "room_message": room_message}
    return render(request, 'blog/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    roomform = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect("home")
        # roomform = RoomForm(request.POST)
        # if roomform.is_valid():
        #     roomform.save(commit=False)
        #     roomform.host = request.user
        #     roomform.save()
        #     return redirect('home')
    context = {"roomform": roomform, "topics": topics}
    return render(request, 'blog/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    roomform = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed in this room")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {"roomform": roomform, "topics": topics, "room": room}
    return render(request, 'blog/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.user:
        return HttpResponse("You are not allowed in this room")
    if request.method == 'POST':
        room.save()
        return redirect('home')
    return render(request, 'blog/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed in this room")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'blog/delete.html', {'obj': message})


@login_required(login_url='login')
def editUser(request):
    user = request.user
    form = UserFrom(instance=user)
    if request.method == 'POST':
        form = UserFrom(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)
    return render(request, 'blog/edit-user.html', {"form": form})


def mobileTopics(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "blog/topicsmobile.html", {"topics": topics})


def activity_mobile(request):
    room_messages = Message.objects.all()
    return render(request, "blog/activity_mobile.html", {"room_messages": room_messages})
