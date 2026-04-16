from __future__ import annotations

import logging
from datetime import UTC, datetime

from django.contrib.gis.geos import Point

from emerald_heart.hints import ResponseType
from emerald_heart.views.core import EmeraldView

LOG = logging.getLogger(__name__)


class LocationData(EmeraldView):
    """Track the location of a user."""

    template_name = "null.html"

    def hx_post(self, request, *args, **kwargs) -> ResponseType:
        latitude = request.POST.get("latitude", None)
        if latitude:
            try:
                lat = float(latitude)
            except Exception:
                return self.render({})
        else:
            lat = 0.0  # Not really necessary but helps the type checker

        longitude = request.POST.get("longitude", None)
        if longitude:
            try:
                lon = float(longitude)
            except Exception:
                lon = 0.0
                return self.render({})
        else:
            lon = 0.0  # Not really necessary but helps the type checker

        try:
            point = Point(lon, lat, srid=3857)
        except Exception:
            LOG.exception("Invalid point value from lat %s long %s", lat, lon)
            return self.render_template("null.html", {})

        user = request.user
        user.current_location = point
        user.save()
        request.session["last-location-check"] = datetime.now(UTC).isoformat()
        LOG.debug("Set %s location to %s", user.display_name, point)

        return self.render({})
