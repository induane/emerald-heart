from __future__ import annotations

import logging

from django.conf import settings
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import QuerySet

LOG = logging.getLogger(__name__)


class CustomPaginate(Paginator):
    """Custom pagination class which keeps track of the page range internally."""

    first_page = 1

    @property
    def page_set(self):
        try:
            return self._page_set
        except AttributeError:
            self._page_set = set(self.page_range)
        return self._page_set

    @property
    def last_page(self):
        return self.num_pages


def paginate(*, queryset: QuerySet, request, **kwargs) -> CustomPaginate | QuerySet | Page:
    """Paginate a queryset."""
    per_page = kwargs.get("per_page", settings.PAGINATION_THRESHOLD)
    surrounding_range = kwargs.get("surrounding_range", 2)

    page = request.GET.get("page", "")
    if page.lower() == "all":
        LOG.debug("Returning all results (not paginating)")
        return queryset

    # Setup paginator
    paginator = CustomPaginate(queryset, per_page)

    try:
        item_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page by default
        item_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of results.
        item_list = paginator.page(paginator.num_pages)

    prev_pages = []
    next_pages = []
    for i in range(1, surrounding_range + 1):
        prev = item_list.number - i
        if prev in paginator.page_set:
            prev_pages.append(prev)
        next = item_list.number + i
        if next in paginator.page_set:
            next_pages.append(next)

    item_list.next_pages = sorted(next_pages)  # type: ignore
    item_list.prev_pages = sorted(prev_pages)  # type: ignore

    return item_list
