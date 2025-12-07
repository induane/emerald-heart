from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime

from django.db import models

from .mixins import BaseMixin

LOG = logging.getLogger(__name__)


class InviteKey(BaseMixin, models.Model):
    """A one-time invitation key for creating accounts."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    expires = models.DateField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    """If an email is given, this flag is toggled once an email has been sent."""

    @property
    def display_name(self) -> str:
        if self.email:
            return f"{self.email}: {self.id}"
        else:
            return str(self.id)

    @property
    def is_expired(self) -> bool:
        if not self.expires:
            return False  # No expiration
        return datetime.now(UTC) >= self.expires

    class Meta:
        """Meta information about the model."""

        ordering = ("-created",)
        app_label = "emerald_heart"
