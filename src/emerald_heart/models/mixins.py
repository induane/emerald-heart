from __future__ import annotations

import logging
from collections import OrderedDict
from typing import cast

from django.db import models

LOG = logging.getLogger(__name__)
SENTINEL = object()


class BaseMixin:
    """Mixin to apply __str__ and __bytes__ to display_name."""

    @property
    def model_name(self) -> str:
        """Return the name of the class."""
        return self.__class__.__name__

    def __str__(self) -> str:
        """Return display_name as unicode string."""
        return self.display_name

    @property
    def display_dict(self) -> OrderedDict[str, object]:
        field_list: list[str] = []
        for field in self._meta.get_fields():  # type: ignore
            if isinstance(field, models.ManyToOneRel | models.ManyToManyField | models.ForeignKey):
                continue
            if (field_name := field.name) not in ("id", "pk_id", "pk"):
                LOG.debug("Field Name: %s (%s)", field.name, type(field.name))
                field_list.append(field.name)

        data = OrderedDict()
        for field_name in sorted(field_list):
            value = getattr(self, field_name, SENTINEL)
            if value is SENTINEL:
                continue
            data[field_name.replace("_", " ").title()] = value
        LOG.debug("Data: %s", data)
        return cast(OrderedDict[str, object], data)

    @property
    def display_name(self) -> str:
        """Default display_name property."""
        return f"{self.__class__.__name__}: {getattr(self, 'id', '')}"
