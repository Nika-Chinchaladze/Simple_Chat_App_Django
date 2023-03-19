from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index-page"),
    path("<str:room>", views.room, name="room-page")
]