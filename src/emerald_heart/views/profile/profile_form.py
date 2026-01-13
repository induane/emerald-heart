from __future__ import annotations

import logging

from emerald_heart import models
from emerald_heart.views.core_form import ModelFormBase

LOG = logging.getLogger(__name__)


class UpdateProfile(ModelFormBase):
    """Update a supervisor user."""

    field_order: tuple[str, ...] = ("first_name", "last_name", "timezone", "email")

    class Meta:
        """Meta information about the form."""

        model = models.User
        fields = ("first_name", "last_name", "timezone", "email")
