# -*- coding: utf-8 -*-
"""Place Python model for the Météo-France REST API."""
import sys
from typing import Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict


class PlaceData(TypedDict):
    """Describe the structure of the API returned place object."""

    insee: str
    name: str
    lat: float
    lon: float
    country: str
    admin: str
    admin2: str
    postCode: str  # noqa: N815


class Place:
    """Class to access the results of 'places' API command."""

    def __init__(self, raw_data: PlaceData):
        """Initialize a Place object."""
        self.raw_data = raw_data

    def __repr__(self) -> str:
        """Return string representation of this class."""
        return "<{}(name={}, country={}, admin={})>".format(
            self.__class__.__name__, self.name, self.country, self.admin
        )

    def __str__(self) -> str:
        """Provide an easy way to identify the Place.

        examples: `Toulouse - (31)` or `Montréal - (Quebec)`
        """
        if self.country == "FR":
            return f"{self.name} - {self.admin} ({self.admin2}) - {self.country}"

        return f"{self.name} - {self.admin} - {self.country}"

    @property
    def insee(self) -> Optional[str]:
        """Return the INSEE ID of the place."""
        return self.raw_data.get("insee")

    @property
    def name(self) -> str:
        """Return the name of the place."""
        return self.raw_data["name"]

    @property
    def latitude(self) -> float:
        """Return the latitude of the place."""
        return self.raw_data["lat"]

    @property
    def longitude(self) -> float:
        """Return the longitude of the place."""
        return self.raw_data["lon"]

    @property
    def country(self) -> str:
        """Return the country code of the place."""
        return self.raw_data["country"]

    @property
    def admin(self) -> Optional[str]:
        """Return the admin of the place.

        Seems to be the department in text ex: "Gers".
        """
        return self.raw_data.get("admin")

    @property
    def admin2(self) -> Optional[str]:
        """Return the admin2 of the place.

        Seems to be the department in numbers "32".
        """
        return self.raw_data.get("admin2")

    @property
    def postal_code(self) -> Optional[str]:
        """Return the postal code of the place."""
        return self.raw_data.get("postCode")
