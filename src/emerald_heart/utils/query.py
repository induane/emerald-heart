from __future__ import annotations

import logging
import re

from django.db.models import Q

LOG = logging.getLogger(__name__)
FIND_TERMS = re.compile(r'"([^"]+)"|(\S+)').findall
NORMALIZE_SPACING = re.compile(r"\s{2,}").sub


def normalize_query(q_str: str) -> list:
    """
    Split a query string into individual items in an array.

    Tweaked from http://stackoverflow.com/questions/14242229/

    Split a query string into individual items in an array, clearing excess
    spaces and grouping together words that were in quotes. For example:

    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    if isinstance(q_str, bytes):
        q_str = q_str.decode("utf-8")
    return [NORMALIZE_SPACING(" ", (x[0] or x[1]).strip()) for x in FIND_TERMS(q_str)]


def build_search_qobj(*, q_str: str, fields: tuple[str, ...], op: str = "icontains") -> Q:
    """Return a query combining Q objects for the given fields."""
    q_obj: Q | None = None
    search_vals = normalize_query(q_str)
    for val in search_vals:
        or_query = None
        for field_name in fields:
            q = Q(**{f"{field_name}__{op}": val})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if or_query is None:
            raise ValueError("No query assembled")
        if isinstance(q_obj, Q):
            q_obj &= or_query
        else:
            q_obj = or_query
    if q_obj is None:
        raise ValueError("No Q object built")
    return q_obj
