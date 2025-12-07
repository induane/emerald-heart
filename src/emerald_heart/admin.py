from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from emerald_heart.models import User


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


admin.site.register(User, EmeraldUserAdmin)
