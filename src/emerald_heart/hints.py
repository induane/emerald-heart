from __future__ import annotations

from typing import BinaryIO, NamedTuple, TextIO, TypeAlias, TypedDict

from boltons.ioutils import SpooledBytesIO
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.utils.functional import Promise

RESPONSE_TYPES: TypeAlias = FileResponse | HttpResponseRedirect | HttpResponse
URL_TYPES: TypeAlias = str | Promise
WritableFile: TypeAlias = BinaryIO | TextIO | SpooledBytesIO
BinaryWritableFile: TypeAlias = BinaryIO | SpooledBytesIO


class SiteActionItem(TypedDict):
    name: str
    icon: str
    action_id: str
    link_url: URL_TYPES
    tooltip: str
    visible: list[str]
    actions: list["SiteActionItem"]


class SiteTab(TypedDict):
    display_name: str
    icon: str
    id: str
    tooltip: str
    link_url: URL_TYPES
    visible: list[str]
    actions: list[SiteActionItem]


class Coordinate(NamedTuple):
    """
    Tuple representing longitude/latitude values.

    Note, this follows EPSG:4326 version 1.1 rules where coordinates are written (longitude, latitude) not the other
    way around. Version 1.0 of EPSG:4326 specifies (latitude, longitude) which really can be confusing. GeoDjango
    PointFields corespond to the 1.1 spec and hence our coordinate value follows this as well.
    """

    longitude: float
    latitude: float


SiteLayout: TypeAlias = list[SiteTab]
