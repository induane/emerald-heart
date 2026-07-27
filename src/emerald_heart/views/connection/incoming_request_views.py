from __future__ import annotations

import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404

from emerald_heart.models import Request
from emerald_heart.utils.paginate import paginate
from emerald_heart.views.core import EmeraldView

LOG = logging.getLogger(__name__)
REQUIRED_GROUPS: tuple[str, ...] = ("admin", "member")


class ListIncomingRequests(EmeraldView):
    """List incoming requests."""

    auth_required = True
    template_name = "item-list-sidebar-2col.html"
    tab_id = "connections"
    action_id = "incoming-requests"
    required_groups = REQUIRED_GROUPS

    def get(self, request, *args, **kwargs):
        page = self.get_page(request)
        search = request.GET.get("q", "")

        q_obj = Q(dest_user=request.user)
        if search:
            search_q_obj = self.get_search_qobj(search, fields=("source_user__name",))
            q_obj &= search_q_obj
        qs = Request.objects.filter(q_obj)
        return self.render(
            {
                "item_list": paginate(queryset=qs, request=request),
                "column_1_name": "Incoming Requests",
                "info_url_name": "member-request-info",
                "item_select_url_name": "member-incoming-request-list-selected",
                "page_number": page,
            }
        )


class ListIncomingRequestsSelected(EmeraldView):
    """List incoming requests with a selection."""

    auth_required = True
    template_name = "item-list-sidebar-2col.html"
    tab_id = "connections"
    action_id = "incoming-requests"
    required_groups = REQUIRED_GROUPS

    def get(self, request, id, *args, **kwargs):
        page = self.get_page(request)
        search = request.GET.get("q", "")

        q_obj = Q(dest_user=request.user)
        if search:
            search_q_obj = self.get_search_qobj(search, fields=("source_user__name",))
            q_obj &= search_q_obj
        qs = Request.objects.filter(q_obj)

        selected = get_object_or_404(Request, pk=id, dest_user=request.user)
        return self.render(
            {
                "item_list": paginate(queryset=qs, request=request),
                "item_dict": selected.display_dict,
                "selected": selected,
                "column_1_name": "Incoming Requests",
                "info_url_name": "member-request-info",
                "item_select_url_name": "member-incoming-request-list-selected",
                "page_number": page,
            }
        )
