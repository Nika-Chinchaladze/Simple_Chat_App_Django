from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index-page"),
    path("room/<str:room>/<str:username>", views.room, name="room-page"),
    path("checkview", views.checkview, name="check-view"),
    path("send", views.send, name="send"),
    path("get-messages/<str:room>/", views.get_message, name="get-message")
]
