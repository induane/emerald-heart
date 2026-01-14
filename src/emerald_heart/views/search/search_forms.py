from __future__ import annotations

import logging
from typing import Any

from django import forms

from emerald_heart.middleware import get_request
from emerald_heart.utils.calendar import utcnow
from emerald_heart.views.core_form import FormBase

LOG = logging.getLogger(__name__)


def get_initial_date():
    """Callable for getting users "today" value."""
    try:
        return get_request().user.today  # type: ignore
    except Exception:
        return utcnow().date()


class SearchForm(FormBase):
    """Custom search form with distance selector."""

    distance = forms.ChoiceField(
        choices=(
            (5, "5 Miles"),
            (10, "10 Miles"),
            (20, "20 Miles"),
            (50, "50 Miles"),
            (100, "100 Miles"),
            (500, "500 Miles"),
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        """Extra form cleaning."""
        data = super().clean()
        try:
            data["distance"] = int(data.get("distance", 100))
        except (TypeError, ValueError):
            self.add_error("distance", "Invalid distance")
            data.pop("distance", None)
        return data
