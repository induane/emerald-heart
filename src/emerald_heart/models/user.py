from __future__ import annotations

import logging
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from emerald_heart.models.mixins import BaseMixin

LOG = logging.getLogger(__name__)


class User(AbstractUser, BaseMixin):
    """Custom user model that adds additional relationships."""

    search_fields = ("name", "id")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=2048, blank=False, null=False, db_index=True)
    is_active = models.BooleanField(default=True)

    @property
    def group_list(self) -> list[str]:
        """Return an array of group names."""
        groups: list[str] = []
        if self_groups := getattr(self, "groups", None):
            groups = self_groups.values_list("name", flat=True)

        return groups

    @property
    def is_admin(self) -> bool:
        """Check if the user is a member of the admin group."""
        if "admin" in self.group_list:
            return True
        else:
            return False

    @property
    def is_developer(self) -> bool:
        """Check if the user is a member of the developer group."""
        if "developer" in self.group_list:
            return True
        else:
            return False

    @property
    def display_name(self) -> str:
        """Default display_name property."""
        if self.name:
            return str(self.name)
        if self.last_name and not self.first_name:
            return str(self.last_name)
        if self.first_name and not self.last_name:
            return str(self.first_name)
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return super().__str__()

    class Meta:
        """Meta information about the model."""

        ordering = ("username",)
        app_label = "emerald_heart"
