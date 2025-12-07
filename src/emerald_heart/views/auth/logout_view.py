from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.http import HttpRequest

from emerald_heart.hints import ResponseType
from emerald_heart.views.core import EmeraldView

LOG = logging.getLogger(__name__)


class EmeraldLogout(EmeraldView):
    """Logout view which handles both regular logouts and htmx logouts."""

    template_name = "core.html"
    auth_required = False

    def post(self, request: HttpRequest) -> ResponseType:
        """Log out the user in the traditional way."""
        auth_logout(request)
        return self.redirect(settings.LOGOUT_REDIRECT_URL)

    def hx_post(self, request: HttpRequest) -> ResponseType:
        """Log out the user using HTMX."""
        auth_logout(request)
        return self.hx_redirect(settings.LOGOUT_REDIRECT_URL)

    def get(self, request: HttpRequest) -> ResponseType:
        """Log out the user in the traditional way."""
        auth_logout(request)
        return self.redirect(settings.LOGOUT_REDIRECT_URL)

    def hx_get(self, request: HttpRequest) -> ResponseType:
        """Log out the user using HTMX."""
        auth_logout(request)
        return self.hx_redirect(settings.LOGOUT_REDIRECT_URL)
