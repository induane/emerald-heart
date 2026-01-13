# Standard
from __future__ import annotations

import logging
import time
from collections import defaultdict
from datetime import UTC, datetime

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

LOG = logging.getLogger(__name__)

ZoneInfo = zoneinfo.ZoneInfo
"""ZoneInfo class; stashed to avoid repeated lookups"""


def get_server_tz() -> ZoneInfo:
    """Return the server time as a timezone aware datetime value."""
    u = datetime.utcnow()
    keymap = defaultdict(list)
    for zone in zoneinfo.available_timezones():
        tz = ZoneInfo(zone)
        keymap[tz.tzname(u)].append(tz)

    server_tz = time.tzname[time.localtime().tm_isdst]
    zones = keymap[server_tz]

    for z in zones:
        if "America" in z.key:
            return z  # Prefer American TZ data

    try:
        return zones[0]  # Fallback to the first one
    except IndexError as ie:
        raise ValueError(f"Unable to find valid zoneinfo for server timezone: {server_tz}") from ie


def utcnow() -> datetime:
    """Return a timezone aware utcnow datetime object."""
    return datetime.now(UTC)


def is_naive(dt: datetime) -> bool:
    """Determine if a datetime object is naive."""
    if dt.tzinfo is None:
        return True
    if dt.tzinfo.utcoffset(dt) is None:
        return True
    return False
