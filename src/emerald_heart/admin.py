from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import GISModelAdmin

from emerald_heart.models import Location, User


class EmeraldUserAdmin(UserAdmin):
    """Custom admin for users."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "bio",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = ("username", "email")
    filter_horizontal = ("groups", "user_permissions")


class LocationAdmin(GISModelAdmin):
    list_display = ("id", "location", "created", "modified")
    readonly_fields = ("id", "created", "modified")


admin.site.register(User, EmeraldUserAdmin)
admin.site.register(Location, LocationAdmin)
