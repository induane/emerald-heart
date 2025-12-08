from __future__ import annotations

import logging

from django.contrib.gis.forms import PointField
from django.contrib.gis.forms.widgets import OSMWidget

from emerald_heart import models
from emerald_heart.views.core_form import ModelFormBase

LOG = logging.getLogger(__name__)


class LocationForm(ModelFormBase):
    """Update or create a Location."""

    field_order: tuple[str, ...] = ("name", "location")
    location = PointField(
        widget=OSMWidget(
            attrs={
                "map_width": 600,
                "map_height": 400,
                "default_lat": 38.949572260845641,
                "default_lon": -95.26347185174219,
                "default_zoom": 12,
            }
        )
    )

    class Meta:
        """Meta information about the form."""

        model = models.Location
        fields = ("name", "location")
