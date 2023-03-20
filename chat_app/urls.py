from django.urls import path
from . import views


urlpatterns = [
    path("", views.start, name="start-page"),
    path("personal", views.personal_page, name="personal-page"),
    path("room/<str:room>/<str:username>", views.room, name="room-page"),
    path("checkview", views.checkview, name="check-view"),
    path("send", views.send, name="send"),
    path("get-messages/<str:room>/", views.get_message, name="get-message"),
    path("register", views.register_user, name="register-user"),
    path("login", views.login_user, name="login-user"),
    path("logout", views.logout_user, name="logout-user")
]
