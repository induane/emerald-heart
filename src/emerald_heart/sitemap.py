from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticPages(Sitemap):
    """Sitemap details for static pages that do not change frequently."""

    def items(self) -> tuple[str, ...]:
        return ("robots-txt", "ai-txt")

    def changefreq(self, item: str) -> str:
        match item:
            case "robots-txt" | "ai-txt":
                return "monthly"
            case _:
                return "weekly"

    def location(self, item: str) -> str:  # type: ignore
        return str(reverse(item))


sitemap_data: dict[str, type[Sitemap]] = {
    "static": StaticPages,
}
"""A map of all sitemap information."""
