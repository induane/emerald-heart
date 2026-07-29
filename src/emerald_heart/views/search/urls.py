from __future__ import annotations

from django.urls import path

from .search import MemberSearch, ViewMember

urlpatterns = [
    path("", MemberSearch.as_view(), name="member-search"),
    path("view/<uuid:id>/", ViewMember.as_view(), name="member-view"),
]
