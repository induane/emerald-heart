from __future__ import annotations

import logging
from functools import cached_property
from typing import Any, Sequence
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import AnonymousUser
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render as render_template
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views.generic import View

from emerald_heart.hints import ResponseType, UrlType
from emerald_heart.models import User
from emerald_heart.utils.render import HttpResponseHXRedirect

LOG = logging.getLogger(__name__)
REDIRECT_FIELD = REDIRECT_FIELD_NAME or "next"
"""Field name for the default redirect field."""


class EmeraldView(View):
    """Base class for most Emerald Heart views."""

    template_name: str = ""
    tab_id: str = ""
    auth_required: bool = True
    required_groups: tuple[str, ...] | list[str] = ()

    def get_context_data(self, request: HttpRequest, *args, **kwargs) -> dict[str, Any]:
        return {}

    def has_permission(self, request: HttpRequest, *args, **kwargs) -> bool:
        """
        Check if user is allowed to access this view.

        A method which can be implemented by subclasses to add additional
        permission checks. By default in the base class this assumes True.
        """
        return True

    def has_group_permission(self) -> bool:
        """
        Determine if the user is a member of one of the allowed groups.

        When no groups are set on the view we interpret that as all users are allowed
        access. Additionally admin or developer users gain access to all views.
        """
        if not self.required_groups:
            return True

        req_groups = {"admin", "developer"} | set(self.required_groups)
        if self.overlap(req_groups, self.user_groups):
            return True
        else:
            return False

    @staticmethod
    def reverse(*args, **kwargs) -> UrlType:
        """Reverse a url from it's given name & args."""
        return reverse_lazy(*args, **kwargs)

    @staticmethod
    def overlap(x: Sequence[str] | set[str], y: Sequence[str] | set[str]) -> bool:
        """Given two iterables, determine if they have any items in common."""
        return bool(set(x) & set(y))

    @cached_property
    def user(self) -> User | AnonymousUser:
        """Try to retrieve the user."""
        return self._request.user

    @cached_property
    def user_groups(self) -> set[str]:
        """Return a list of all groups the current user is in."""
        user = getattr(self, "user", None)
        if isinstance(user, AnonymousUser):
            return {"anonymous"}
        elif user is None:
            return {"anonymous"}
        try:
            return set(self.user.group_list)
        except Exception:
            LOG.exception("Unable to get user groups")
            return {"anonymous"}

    @property
    def tabs(self) -> list[dict[str, Any]]:
        """Determine allowed tabs & actions."""
        allowed_tabs = []
        for tab in settings.SITE_DATA[::-1]:
            tab_groups = {"admin", "developer"} | set(tab["visible"])
            if self.overlap(self.user_groups, tab_groups) or not tab["visible"]:
                allowed_actions = []
                for action in tab["actions"]:
                    act_groups = {"admin", "developer"} | set(action["visible"])
                    if self.overlap(act_groups, self.user_groups) or not action["visible"]:
                        allowed_actions.append(action)
                tab["actions"] = allowed_actions
                allowed_tabs.append(tab)
        return allowed_tabs

    @property
    def tab_id_list(self) -> list[str]:
        """Return an iterable of tab ids."""
        return [x["id"] for x in self.tabs]

    @property
    def actions(self) -> list[dict[str, Any]]:
        """Return an iterable of all actions for the current tab."""
        LOG.debug("Processing actions for tab.")
        for tab in self.tabs:
            if tab["id"] == self.tab_id:
                return tab["actions"]
        else:
            return []

    def redirect(self, url: str) -> HttpResponseRedirect:
        """Return a redirect to the given url."""
        return HttpResponseRedirect(url)

    def hx_redirect(self, url: str) -> HttpResponseHXRedirect:
        """Return a redirect to the given url with htmx headers."""
        return HttpResponseHXRedirect(url)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # Attach a few attributes to the view instance
        self._request = request
        self._request_args = args
        self._request_kwargs = kwargs

        # Stash a few lookup checks (they're added via middleware so type checking doesn't work)
        is_htmx: bool = request.is_htmx  # type:ignore
        is_boosted: bool = request.is_boosted  # type:ignore
        user = request.user  # type:ignore

        if not user.is_authenticated and self.auth_required is True:
            resolved_url = resolve_url(reverse_lazy("auth-login"))
            login_url_parts = list(urlparse(resolved_url))
            querystring = QueryDict(login_url_parts[4], mutable=True)
            querystring[REDIRECT_FIELD] = request.path
            login_url_parts[4] = querystring.urlencode(safe="/")
            final_url = urlunparse(login_url_parts)
            if is_htmx:
                return HttpResponseHXRedirect(final_url)
            else:
                return HttpResponseRedirect(final_url)

        if not self.has_permission(request, *args, **kwargs):
            LOG.info("Permission check failed for %s", self.user)
            raise Http404  # User not allowed to see page

        if not self.has_group_permission():
            LOG.debug(
                "User %s is not a member of %s",
                self.user,
                ", ".join(self.required_groups) if self.required_groups else "",
            )
            raise Http404

        # Dispatch htmx requests to their own handlers unless they are boosted links. Boosted links indicate a request
        # for a fully rendered page template.
        if is_htmx and not is_boosted:
            match request.method:
                case "DELETE":
                    htmx_method = getattr(self, "hx_delete", None)
                case "GET":
                    htmx_method = getattr(self, "hx_get", None)
                case "PATCH":
                    htmx_method = getattr(self, "hx_patch", None)
                case "POST":
                    htmx_method = getattr(self, "hx_post", None)
                case "PUT":
                    htmx_method = getattr(self, "hx_put", None)
                case _:
                    raise Http404(f"Unknown verb {request.method}")

            # This warning fires when the request is an htmx request but the view class didn't implement
            # an hx_<verb> method to handle it. For this case it will use the normal verb handler (self.get,
            # self.post, etc...)
            if htmx_method is None:
                LOG.warning(
                    "hx_%s is not implemented for %s; falling back to default %s",
                    request.method.lower(),
                    self.__class__,
                    request.method.lower(),
                )
            else:
                return htmx_method(request, *args, **kwargs)

        # Either the request wasn't an HTMX request or it was a boosted link, use normal dispatch.
        return super().dispatch(request, *args, **kwargs)

    def render_template(
        self,
        template_name: str,
        context: dict[str, Any] | None = None,
        *,
        content_type: str | None = None,
    ) -> ResponseType:
        """
        Like `render` but requires a template argument.

        This is useful if you need to render a different template when returning than the default view
        template::

            return self.render_template("partials/form.html", my_context)
        """
        context_data = self.get_context_data(self._request, *self._request_args, **self._request_kwargs)
        if context is not None:
            context_data.update(context)
        return self.render(context_data, template_name=template_name, content_type=content_type)

    def render(
        self,
        context: dict[str, Any] | None = None,
        *,
        template_name: str | None = None,
        content_type: str | None = None,
    ) -> ResponseType:
        """Render the page, adding given context to default context."""
        context_data = self.get_context_data(self._request, *self._request_args, **self._request_kwargs)
        if context is not None:
            context_data.update(context)
        return render_template(
            self._request,
            template_name or self.template_name,
            context_data,
            content_type=content_type,
        )
