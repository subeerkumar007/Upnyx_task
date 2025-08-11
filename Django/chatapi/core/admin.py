from django.contrib import admin

from .models import User, Chat, AuthToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "tokens")
    search_fields = ("username",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")
    search_fields = ("user__username", "message", "response")
    list_filter = ("timestamp",)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created")
    search_fields = ("user__username", "key")


