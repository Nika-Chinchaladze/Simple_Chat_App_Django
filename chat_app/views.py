from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterModelForm, LoginModelForm, HomeForm, SearchForm
from .models import Room, Message, RoomUsers

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
    form1 = HomeForm()
    form2 = SearchForm()
    present_user = request.user
    all_rooms = Room.objects.all()
    my_rooms = all_rooms.filter(user=present_user).all()

    all_room_users = RoomUsers.objects.values_list("username_room", flat=True)
    used_rooms = []
    for item in list(all_room_users):
        if item.split("^")[0] == present_user.username:
            concrete_room = all_rooms.filter(name=item.split("^")[-1]).first()
            used_rooms.append(concrete_room)
    
    return render(request, "chat/home.html", {
        "form1": form1,
        "form2": form2,
        "user": present_user,
        "my_rooms": my_rooms,
        "used_rooms": used_rooms
    })


@login_required
def room(request, room, username):
    present_user = request.user
    if request.method == "POST":
        room_object = Room.objects.get(id=request.POST["room_id"])
        message = request.POST["message"]

        new_message = Message(
            value=message,
            user=present_user,
            room=room_object
        )
        new_message.save()
        return HttpResponseRedirect(reverse("room-page", kwargs={
            "room": room_object.name,
            "username": present_user.username
        }))

    room_details = Room.objects.get(name=room)
    return render(request, "chat/room.html", {
        "room": room,
        "username": username,
        "room_details": room_details,
        "user": present_user
    })


@login_required
def get_messages(request, room):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if is_ajax:
        if request.method == "GET":
            room_details = Room.objects.get(name=room)
            room_messages = Message.objects.filter(room=room_details).all()
            return JsonResponse({
                "messages": list(room_messages.values())
            })
        else:
            return JsonResponse({
                "status": "Invalid Request"
            })
    else:
        HttpResponseBadRequest("Invalid Request")


def room_users(request, room, username):
    check_user = RoomUsers.objects.values_list("username_room", flat=True)
    check_point = f"{username}^{room}"
    if check_point in list(check_user):
        pass
    else:
        new_room_user = RoomUsers(
            username_room=check_point
        )
        new_room_user.save()
    return HttpResponseRedirect(reverse("room-page", kwargs={
        "room": room,
        "username": username
    }))


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
            new_room = Room(name=room_name, user=present_user)
            new_room.save()
            return HttpResponseRedirect(reverse("personal-page"))


@login_required
def searchview(request):
    present_user = request.user
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data["room_name"]
            searched_room = Room.objects.filter(name=room_name).first()
            if searched_room is not None:
                return render(request, "chat/search.html", {
                    "searched_room": searched_room,
                    "user": present_user
                })
            else:
                messages.error(request, "Not Found")
                return HttpResponseRedirect(reverse("personal-page"))


@login_required
def all_rooms(request):
    present_user = request.user
    rooms = Room.objects.all()
    return render(request, "chat/all.html", {
        "rooms": rooms,
        "user": present_user
    })


@login_required
def delete_room(request, room_id, room_name):
    present_user = request.user
    # delete chosen room:
    chosen_room = Room.objects.get(id=room_id)
    chosen_room.delete()
    # delete room - users:
    all_room_users = RoomUsers.objects.all()
    for item in all_room_users:
        if item.username_room.split("^")[-1] == room_name:
            item.delete()
    messages.success(request, "Room Has Been Deleted")
    return HttpResponseRedirect(reverse("personal-page"))