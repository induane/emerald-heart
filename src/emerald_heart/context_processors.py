from __future__ import annotations

import logging

from django.conf import settings

LOG = logging.getLogger(__name__)


def site_info(request) -> dict[str, object]:
    """Return site version information and a static int for static files."""
    site_context = {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_NAME_LONG": settings.SITE_NAME_LONG,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        "DEBUG": settings.DEBUG,
    }
    # if not request.user.is_authenticated:
    # site_context["active_tab"] = "logout"
    return site_context
