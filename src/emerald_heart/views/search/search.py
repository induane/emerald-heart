from __future__ import annotations

import logging
from typing import Any

from django.http import HttpRequest

from emerald_heart.hints import ResponseType
from emerald_heart.views.core import EmeraldView
from emerald_heart.views.search.search_forms import SearchForm
from emerald_heart.views.search.search_service import get_member_by_id, get_members

LOG = logging.getLogger(__name__)


class MemberSearch(EmeraldView):
    """A page for searching member profiles."""

    template_name = "member-list.html"
    auth_required = True
    tab_id = "search"

    def get_context_data(self, request: HttpRequest, *args, **kwargs) -> dict[str, Any]:
        return {"submit_text": "Search", "submit_icon": "las la-search"}

    def get(self, request, *args, **kwargs) -> ResponseType:
        form = SearchForm()
        context = {
            "member_list": [],
            "form": form,
            "initial": True,
        }
        return self.render(context)

    def post(self, request, *args, **kwargs) -> ResponseType:
        form = SearchForm(request.POST)
        context = {
            "member_list": [],
            "form": form,
            "initial": False,
        }
        if form.is_valid():
            context["member_list"] = get_members(
                location=self.user.current_location,
                distance=form.cleaned_data["distance"],
            )
            context.update(form.cleaned_data)
        else:
            LOG.error(form.errors)
        return self.render(context)


class ViewMember(EmeraldView):
    """View a member profile."""

    auth_required = True
    tab_id = "search"
    # TEMPLATE_NAME = "player/coach-profile.html"

    def get(self, request, id, *args, **kwargs) -> ResponseType:
        return self.render({"member": get_member_by_id(id)})
