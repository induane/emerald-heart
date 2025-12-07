from __future__ import annotations

import logging

from django.http.response import HttpResponseRedirectBase

LOG = logging.getLogger(__name__)


class HttpResponseHXRedirect(HttpResponseRedirectBase):
    """An HttpResponseRedirect that adds an HX-Redirect header so HTMX redirects also work."""

    status_code = 200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]
        del self["Location"]
