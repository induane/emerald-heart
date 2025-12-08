from __future__ import annotations

import logging
from typing import cast

from django import forms
from django.http import HttpRequest

from emerald_heart.middleware import get_request
from emerald_heart.models import User

LOG = logging.getLogger(__name__)


class ModelFormBase(forms.ModelForm):
    """Base class for modelforms."""

    required_css_class = "form-required"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if _meta := getattr(self, "Meta", None):
            for field in getattr(_meta, "required", ()):
                self.fields[field].required = True

            for field in getattr(_meta, "not_required", ()):
                self.fields[field].required = False

    @property
    def is_edit(self) -> bool:
        """Determine whether the current instance is an edit form."""
        if getattr(self, "instance", None) and self.instance.pk:
            return True
        return False

    @property
    def request(self) -> HttpRequest:
        """Return the current request from thread local."""
        return get_request()

    @property
    def user(self) -> User:
        return cast(User, self.request.user)  # type: ignore
