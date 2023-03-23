from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterModelForm, LoginModelForm, HomeForm
from .models import Room, Message

# Create your views here.



# ====================================== AUTHENTICATION SECTION ======================================= #
def register_user(request):
    present_user = request.user
    if request.method == "POST":
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            form.save()
            current_user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"]
            )
            login(request, current_user)
            return HttpResponseRedirect(reverse("personal-page"))
    else:
        form = RegisterModelForm()
        return render(request, "chat/register.html", {
            "form": form,
            "user": present_user
        })


def login_user(request):
    present_user = request.user
    if request.method == "POST":
        form = LoginModelForm(request, data=request.POST)
        if form.is_valid():
            current_user = form.get_user()
            if current_user is not None:
                login(request, current_user)
                return HttpResponseRedirect(reverse("personal-page"))
    else:
        form = LoginModelForm()
        return render(request, "chat/login.html", {
            "form": form,
            "user": present_user
        })


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("login-user"))


# ====================================== ENDING SECTION ======================================= #
def start(request):
    return HttpResponseRedirect(reverse("login-user"))


@login_required
def personal_page(request):
    form = HomeForm()
    current_user = request.user
    available_rooms = Room.objects.all()
    return render(request, "chat/home.html", {
        "form": form,
        "user": current_user,
        "rooms": available_rooms
    })


@login_required
def room(request, room, username):
    present_user = request.user
    room_details = Room.objects.get(name=room)
    return render(request, "chat/room.html", {
        "room": room,
        "username": username,
        "room_details": room_details,
        "user": present_user
    })


@login_required
def checkview(request):
    present_user = request.user
    if request.method == "POST":
        room_name = request.POST["room_name"]
        user_name = present_user.username

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


@login_required
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


@login_required
def get_message(request, room):
    chosen_room = Room.objects.get(name=room)
    messages = Message.objects.filter(room=chosen_room).all()
    return JsonResponse({
        "messages": list(messages.values())
    })
