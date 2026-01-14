from __future__ import annotations

import logging
import math

LOG = logging.getLogger(__name__)


def distance_to_degrees(distance: float, latitude: float):
    """Convert distance (in meters) to degrees."""
    lat_radians = latitude * (math.pi / 180)
    # 1 longitudinal degree at the equator equal 111,319.5m equiv to 111.32km
    return distance / (111_319.5 * math.cos(lat_radians))
