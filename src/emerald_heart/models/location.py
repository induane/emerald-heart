from __future__ import annotations

import logging
import uuid

from django.contrib.gis.db import models as gis_models
from django.db import models

from emerald_heart.hints import Coordinate

from .mixins import BaseMixin

LOG = logging.getLogger(__name__)


class Location(models.Model, BaseMixin):
    """A generic GIS single-point location."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    location = gis_models.PointField(unique=True, geography=False, srid=3857)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "emerald_heart.User",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="location_set",
    )

    @property
    def display_name(self) -> str:
        return f"({self.longitude}, {self.latitude})"

    def __str__(self):
        return self.display_name

    @property
    def latitude(self) -> float:
        return self.location.y

    @property
    def longitude(self) -> float:
        return self.location.x

    @property
    def google_maps_url(self) -> str:
        return f"https://maps.google.com/?q={self.latitude},{self.longitude}"

    @property
    def coordinates(self) -> Coordinate:
        """
        Return the GPS coordinates in latitude, longitude form.

        Note, this follows EPSG:4326 version 1.1 rules where coordinates are written (longitude, latitude) not the
        other way around. Version 1.0 of EPSG:4326 specifies (latitude, longitude) which really can be confusing.
        GeoDjango PointFields corespond to the 1.1 spec and hence our coordinate value follows this as well.
        """
        return Coordinate(self.location.x, self.location.y)

    class Meta:
        """Meta information about the model."""

        ordering = ("-created",)
        app_label = "emerald_heart"
