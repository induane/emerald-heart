from __future__ import annotations

import logging

from emerald_heart.views.core import EmeraldView

from .location_form import LocationForm

LOG = logging.getLogger(__name__)


class CreateLocation(EmeraldView):
    """Create a new Location."""

    auth_required = True
    template_name = "form.html"
    tab_id = "user-profile"

    def get(self, request, *args, **kwargs):
        return self.render(
            {
                "form": LocationForm(),
                "cancel_url": self.reverse("user-profile"),
            }
        )

    def post(self, request, *args, **kwargs):
        form = LocationForm(data=request.POST)
        if form.is_valid():
            LOG.debug("form valid")
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return self.redirect(self.reverse("user-profile"))
        LOG.debug("form invalid %s", form.errors)
        return self.render({"form": form, "cancel_url": self.reverse("user-profile")})

    def hx_post(self, request, *args, **kwargs):
        form = LocationForm(data=request.POST)
        if form.is_valid():
            LOG.debug("form valid")
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return self.hx_redirect(self.reverse("user-profile"))
        LOG.debug("form invalid %s", form.errors)
        return self.render_template("partial/form.html", {"form": form, "cancel_url": self.reverse("user-profile")})
