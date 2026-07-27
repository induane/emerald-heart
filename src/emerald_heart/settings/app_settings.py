from __future__ import annotations

from django.urls import reverse_lazy

from emerald_heart.hints import SiteLayout

from .base import *  # noqa

SITE_NAME = "Emerald Directory"
SITE_NAME_LONG = "Emerald Community Directory"
SITE_DESCRIPTION = "A directory and community oriented application."

THUMBNAIL_SIZE = 256
"""Default size of thumbnail (in pixels) to generate when uploading images."""

PAGINATION_THRESHOLD = 10
"""Number if items to show before beginning to paginate the view."""


LOGIN_TAB: SiteLayout = [
    {
        "display_name": "Logout",
        "id": "logout",
        "icon": "la-sign-out-alt",
        "tooltip": "Logout",
        "link_url": reverse_lazy("auth-logout"),
        "visible": [],
        "actions": [],
    }
]

SITE_DATA: SiteLayout = [
    {
        "display_name": "Search",
        "id": "search",
        "icon": "la-search-location",
        "tooltip": "Search for members by distance",
        "link_url": reverse_lazy("member-search"),
        "visible": [],
        "actions": [],
    },
    {
        "display_name": "Profile",
        "id": "user-profile",
        "icon": "la-user-circle",
        "tooltip": "User Profile",
        "link_url": reverse_lazy("user-profile"),
        "visible": [],
        "actions": [],
    },
    {
        "display_name": "Connections",
        "id": "connections",
        "icon": "la-link",
        "tooltip": "Connections & Connection Requests",
        "link_url": reverse_lazy("member-incoming-request-list"),
        "visible": [],
        "actions": [
            {
                "name": "Requests",
                "icon": "la-unlink",
                "action_id": "incoming-requests",
                "link_url": reverse_lazy("member-incoming-request-list"),
                "tooltip": "View incoming connection requests",
                "visible": [],
                "actions": [],
            },
            {
                "name": "Pending",
                "icon": "la-external-link-alt",
                "action_id": "outgoing-requests",
                "link_url": reverse_lazy("member-outgoing-request-list"),
                "tooltip": "View my pending outgoing requests",
                "visible": [],
                "actions": [],
            },
        ],
    },
]
