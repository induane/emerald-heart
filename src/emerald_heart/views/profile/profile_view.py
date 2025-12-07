from __future__ import annotations

import logging

from emerald_heart.hints import ResponseType
from emerald_heart.views.core import EmeraldView

from .profile_form import UpdateProfile

LOG = logging.getLogger(__name__)


class UserProfile(EmeraldView):
    """Display a profile of the logged in user."""

    auth_required = True
    template_name = "user-profile.html"
    tab_id = "user-profile"

    def get(self, request, *args, **kwargs) -> ResponseType:
        return self.render(
            {
                "user": self.user,
                "change_password_link": "#",
                "edit_profile_link": self.reverse("user-profile-edit"),
            }
        )


class EditProfile(EmeraldView):
    """Edit a users profile."""

    auth_required = True
    template_name = "form.html"
    tab_id = "user-profile"

    def get(self, request, *args, **kwargs):
        return self.render(
            {
                "form": UpdateProfile(instance=request.user),
                "cancel_url": self.reverse("user-profile"),
            }
        )

    def post(self, request, *args, **kwargs):
        form = UpdateProfile(instance=self.user, data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return self.redirect(self.reverse("user-profile"))
        return self.render({"form": form, "cancel_url": self.reverse("user-profile")})

    def hx_post(self, request, *args, **kwargs):
        form = UpdateProfile(instance=self.user, data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return self.hx_redirect(self.reverse("user-profile"))
        return self.render_template("partial/form.html", {"form": form, "cancel_url": self.reverse("user-profile")})
