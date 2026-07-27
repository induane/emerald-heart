from __future__ import annotations

import logging
import uuid
from collections import OrderedDict
from typing import cast

from django.db import models

from .mixins import BaseMixin

LOG = logging.getLogger(__name__)


class Request(BaseMixin, models.Model):
    """A request for one user to connect to another."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    source_user = models.ForeignKey(
        "emerald_heart.User",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="user_outgoing_requests",
    )
    dest_user = models.ForeignKey(
        "emerald_heart.User",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="user_incoming_requests",
    )
    created = models.DateTimeField(auto_now_add=True)

    @property
    def display_name(self) -> str:
        return f"{self.source_user.display_name} --> {self.dest_user.display_name}"

    @property
    def display_dict(self) -> OrderedDict[str, object]:
        data = OrderedDict()
        data["Created"] = self.created.strftime("%Y-%d-%m")
        data["From User"] = self.source_user.display_name
        data["To User"] = self.dest_user.display_name
        LOG.debug("Data: %s", data)
        return cast(OrderedDict[str, object], data)

    class Meta:
        """Meta information about the model."""

        ordering = ("-created",)
        app_label = "emerald_heart"
