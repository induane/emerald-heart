from __future__ import annotations

import logging
from uuid import UUID

from django.contrib.gis.measure import Distance
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from emerald_heart.models import User
from emerald_heart.utils.spatial import distance_to_degrees

LOG = logging.getLogger(__name__)


def get_all_members(current_user: User | None = None) -> QuerySet[User]:
    """Return all members without filtering."""
    return User.objects.filter(~Q(id=current_user.id) & ~Q(username="admin"))


def get_members(location=None, distance=None, current_user: User | None = None) -> QuerySet[User]:
    """Query for members based on provided data."""
    if distance and location:
        distance_meters = Distance(mi=distance).m
        qobj = Q(current_location__dwithin=(location, distance_to_degrees(distance_meters, location.y))) & ~Q(
            username="admin"
        )
        if current_user:
            qobj &= ~Q(id=current_user.id)
        return User.objects.filter(qobj).distinct()
    else:
        return get_all_members(current_user=current_user)


def get_member_by_id(id: UUID) -> User:
    """Find the member that matches the given user id."""
    return get_object_or_404(User, id=id)
