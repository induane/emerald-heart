from __future__ import annotations

import logging
import time
from threading import local
from typing import cast

from django.http import HttpRequest

from .hints import RESPONSE_TYPES

# Cust object
_appt_thread_local = local()

LOG = logging.getLogger(__name__)

FLOAT_CHARS = "0123456789."
"""Valid characters in a floating point string."""


class MiddlewareBase:
    """Simple generic base class for custom middleware."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> RESPONSE_TYPES:
        return self.get_response(request)


class SimpleProfilingMiddleware(MiddlewareBase):
    """Middleware which logs the time taken to render a page."""

    def __call__(self, request: HttpRequest) -> RESPONSE_TYPES:
        start_time = time.time()
        response = self.get_response(request)
        LOG.info("%s took %.4f seconds: ", request.build_absolute_uri(), time.time() - start_time)
        return response


def set_request(request: HttpRequest) -> None:
    """Stash the request object on thread-local storage."""
    _appt_thread_local.request = request


def get_request() -> HttpRequest:
    """Retrieve the request object from thread-local storage."""
    return cast(HttpRequest, getattr(_appt_thread_local, "request", None))


def unset_request():
    """Remove the request object from thread-local storage."""
    try:
        delattr(_appt_thread_local, "request")
    except AttributeError:
        pass


class RequestMiddleware(MiddlewareBase):
    """Stash the request where it can be retrieved as needed."""

    def __call__(self, request: HttpRequest) -> RESPONSE_TYPES:
        set_request(request)
        response = self.get_response(request)
        unset_request()
        return response


class NoCacheMiddleware(MiddlewareBase):
    """Add no-cache headers to response to avoid client-side caching."""

    def __call__(self, request: HttpRequest) -> RESPONSE_TYPES:
        response = self.get_response(request)
        response["Pragma"] = "no-cache"
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Expires"] = "0"
        return response


class HtmxMiddleware(MiddlewareBase):
    """Add some htmx specific attributes to the request."""

    def __call__(self, request) -> RESPONSE_TYPES:
        get_header = request.headers.get

        # Boolean values
        request.is_htmx = get_header("HX-Request") == "true"
        request.hx_boosted = get_header("HX-Boosted") == "true"
        request.hx_history_restore_request = get_header("HX-History-Restore-Request") == "true"

        # Determine if ajax and if it is async in general
        request.is_ajax = get_header("x-requested-with") == "XMLHttpRequest"
        request.is_async = False
        if request.is_ajax or (request.is_htmx and not request.hx_boosted):
            request.is_async = True

        # Text values
        request.hx_current_url = get_header("HX-Current-URL") or ""
        request.hx_prompt = get_header("HX-Prompt") or ""
        request.hx_target = get_header("HX-Target") or ""
        request.hx_trigger = get_header("HX-Trigger") or ""
        request.hx_trigger_name = get_header("HX-Trigger-Name") or ""
        return self.get_response(request)
