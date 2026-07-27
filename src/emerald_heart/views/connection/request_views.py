from __future__ import annotations

import logging

from django.shortcuts import get_object_or_404

from emerald_heart.models import Request
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
