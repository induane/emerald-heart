from __future__ import annotations

import logging
from datetime import UTC, datetime

from django.conf import settings
from django.utils.dateparse import parse_datetime

LOG = logging.getLogger(__name__)


def site_info(request) -> dict[str, object]:
    """Return site version information and a static int for static files."""
    site_context = {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_NAME_LONG": settings.SITE_NAME_LONG,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        "DEBUG": settings.DEBUG,
        "REQUEST_LOCATION": False,
    }
    if request.user.is_authenticated is True:
        last_check = request.session.get("last-location-check", None)
        if request.user.current_location:
            if not last_check:
                site_context["REQUEST_LOCATION"] = True
            else:
                delta = datetime.now(UTC) - parse_datetime(last_check)
                if delta.total_seconds() > 600:
                    site_context["REQUEST_LOCATION"] = True
                else:
                    site_context["REQUEST_LOCATION"] = False
            pass
        else:
            site_context["REQUEST_LOCATION"] = True

    return site_context
