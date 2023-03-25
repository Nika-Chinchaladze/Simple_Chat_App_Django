from django.urls import path
from . import views


urlpatterns = [
    path("", views.start, name="start-page"),
    path("personal", views.personal_page, name="personal-page"),
    path("room/<str:room>/<str:username>", views.room, name="room-page"),
    path("checkview", views.checkview, name="check-view"),
    path("register", views.register_user, name="register-user"),
    path("login", views.login_user, name="login-user"),
    path("logout", views.logout_user, name="logout-user"),
    path("room-users/<str:room>/<str:username>", views.room_users, name="room-users"),
    path("searchview", views.searchview, name="search-view"),
    path("all-rooms", views.all_rooms, name="all-rooms"),
    path("delete-room/<int:room_id>/<str:room_name>", views.delete_room, name="delete-room"),
    path("get-messages/<str:room>", views.get_messages, name="get-messages"),
    path("send-messages", views.send_messages, name="send-messages")
]
