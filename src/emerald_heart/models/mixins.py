from __future__ import annotations

import logging

LOG = logging.getLogger(__name__)


class BaseMixin:
    """Mixin to apply __str__ and __bytes__ to display_name."""

    @property
    def model_name(self) -> str:
        """Return the name of the class."""
        return self.__class__.__name__

    def __str__(self) -> str:
        """Return display_name as unicode string."""
        return f"{self.__class__.__name__}: {getattr(self, 'id', '')}"

    @property
    def display_name(self) -> str:
        """Default display_name property."""
        return self.__str__()
