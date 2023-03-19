from django.shortcuts import render


from .models import Room, Message
# Create your views here.


def index(request):
    return render(request, "chat/home.html")


def room(request, room):
    return render(request, "chat/room.html")
