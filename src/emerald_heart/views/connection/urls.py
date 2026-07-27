from __future__ import annotations

from django.urls import path

from .incoming_request_views import ListIncomingRequests, ListIncomingRequestsSelected
from .outgoing_request_views import ListOutgoingRequests, ListOutgoingRequestsSelected
from .request_views import RequestInfo

urlpatterns = [
    path(
        "request/outgoing/list/",
        ListOutgoingRequests.as_view(),
        name="member-outgoing-request-list",
    ),
    path(
        "request/outgoing/list/selected/<uuid:id>",
        ListOutgoingRequestsSelected.as_view(),
        name="member-outgoing-request-list-selected",
    ),
    path(
        "request/incoming/list/",
        ListIncomingRequests.as_view(),
        name="member-incoming-request-list",
    ),
    path(
        "request/incoming/list/selected/<uuid:id>",
        ListIncomingRequestsSelected.as_view(),
        name="member-incoming-request-list-selected",
    ),
    path("info/<uuid:id>", RequestInfo.as_view(), name="member-request-info"),
]
