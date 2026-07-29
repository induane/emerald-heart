from __future__ import annotations

import logging

from django.shortcuts import get_object_or_404

from emerald_heart.models import Request, User
from emerald_heart.views.core import EmeraldView

LOG = logging.getLogger(__name__)
REQUIRED_GROUPS: tuple[str, ...] = ("admin", "member")


class RequestInfo(EmeraldView):
    """Render shortform details about a connection requests."""

    auth_required = True
    template_name = "partial/item-info.html"
    tab_id = "connections"
    required_groups = REQUIRED_GROUPS

    def hx_get(self, request, id, *args, **kwargs):
        selected = get_object_or_404(Request, pk=id)
        return self.render({"item_dict": selected.display_dict, "selected": selected})

    def get(self, request, id, *args, **kwargs):
        selected = get_object_or_404(Request, pk=id)
        return self.render({"item_dict": selected.display_dict, "selected": selected})


class CreateRequest(EmeraldView):
    """Create a request between two users and return an empty result."""

    auth_required = True
    template_name = "null.html"
    required_groups = REQUIRED_GROUPS

    def hx_post(self, request, src_id, dest_id, *args, **kwargs):
        src_users = User.objects.filter(id=src_id)
        dest_users = User.objects.filter(id=dest_id)

        try:
            src_user = src_users.first()
            dest_user = dest_users.first()
        except Exception:
            LOG.exception("Unable to find users.")
            return self.render({})

        instance = Request(source_user=src_user, dest_user=dest_user)
        instance.save()
        return self.render({})
