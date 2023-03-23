from django.contrib import admin
from .models import Room, Message, RoomUsers

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class MessageAdmin(admin.ModelAdmin):
    list_display = ("value", "date", "user", "room",)


class RoomUsersAdmin(admin.ModelAdmin):
    list_display = ("username_room",)


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(RoomUsers, RoomUsersAdmin)
