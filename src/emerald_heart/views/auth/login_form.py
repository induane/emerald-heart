from __future__ import annotations

import logging

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

LOG = logging.getLogger(__name__)


class EmeraldAuthForm(AuthenticationForm):
    """A modified login form."""

    username = forms.CharField(
        widget=TextInput(
            attrs={
                "class": "login-username login-input",
                "placeholder": "Username (required)",
                "required": "true",
            }
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "class": "login-password login-input",
                "placeholder": "Password (required)",
                "required": "true",
            }
        )
    )
