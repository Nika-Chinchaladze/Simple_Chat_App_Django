from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterModelForm
from .models import Room, Message

# Create your views here.


def register(request):
    if request.method == "POST":
        pass
    else:
        form = RegisterModelForm()
        return render(request, "chat/register.html", {
            "form": form
        })


def index(request):
    return render(request, "chat/home.html")


def room(request, room, username):
    room_details = Room.objects.get(name=room)
    return render(request, "chat/room.html", {
        "room": room,
        "username": username,
        "room_details": room_details
    })


def checkview(request):
    if request.method == "POST":
        room_name = request.POST["room_name"]
        user_name = request.POST["user_name"]

        if Room.objects.filter(name=room_name).exists():
            return HttpResponseRedirect(reverse("room-page", kwargs={
                "room": room_name,
                "username": user_name
            }))
        else:
            new_room = Room(name=room_name)
            new_room.save()
            return HttpResponseRedirect(reverse("room-page", kwargs={
                "room": room_name,
                "username": user_name
            }))


def send(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        room_object = Room.objects.get(id=request.POST["room_id"])
        message = request.POST["message"]

        new_message = Message(
            value=message,
            user=user_name,
            room=room_object
        )
        new_message.save()
        return HttpResponse("Message has been sent, Successfully!")


def get_message(request, room):
    chosen_room = Room.objects.get(name=room)
    messages = Message.objects.filter(room=chosen_room).all()
    return JsonResponse({
        "messages": list(messages.values())
    })
