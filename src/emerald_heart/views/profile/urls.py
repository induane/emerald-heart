from __future__ import annotations

from django.urls import path

from .location_view import CreateLocation, DeleteLocation
from .profile_view import EditProfile, UserProfile

urlpatterns = [
    path("", UserProfile.as_view(), name="user-profile"),
    path("edit", EditProfile.as_view(), name="user-profile-edit"),
    path("location/create/", CreateLocation.as_view(), name="user-location-create"),
    path("location/delete/<uuid:uuid>/", DeleteLocation.as_view(), name="user-location-delete"),
]
