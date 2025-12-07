from __future__ import annotations

from django.urls import reverse_lazy

from emerald_heart.hints import SiteLayout

from .base import *  # noqa

SITE_NAME = "Emerald Directory"
SITE_NAME_LONG = "Emerald Community Directory"
SITE_DESCRIPTION = "A directory and community oriented application."

THUMBNAIL_SIZE = 256
"""Default size of thumbnail (in pixels) to generate when uploading images."""


LOGIN_TAB: SiteLayout = [
    {
        "display_name": "Logout",
        "id": "logout",
        "la_icon": "la-sign-out-alt",
        "icon": "las la-sign-out-alt",
        "tooltip": "Logout",
        "link_url": reverse_lazy("auth-logout"),
        "visible": [],
        "actions": [],
    }
]

SITE_DATA: SiteLayout = []
