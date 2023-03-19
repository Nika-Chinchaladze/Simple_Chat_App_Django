from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "chat/home.html")


def room(request):
    return render(request, "chat/room.html")
