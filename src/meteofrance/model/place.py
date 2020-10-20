# -*- coding: utf-8 -*-
"""Place Python model for the Météo-France REST API."""
import sys
from typing import Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict


class PlaceData(TypedDict):
    """Describing the data structure of place object returned by the REST API."""

    insee: Optional[str]
    name: str
    lat: float
    lon: float
    country: str
    admin: str
    admin2: Optional[str]
    postCode: Optional[str]  # noqa: N815


class Place:
    """Class to access the results of 'places' REST API request.

    Attributes:
        insee: A string corresponding to the INSEE ID of the place.
        name: Name of the place.
        lat: A float with the latitude in degree of the place.
        lon: A float with the longitude in degree of the place
        country: A string corresponding to the country code of the place.
        admin: A string with the name of the administrative area ('Département' for
            France and Region for other countries).
        admin2: A string correponding to an administrative code ( 'Département' number
            for France)
        postCode: A string corresponding to the ZIP code of location.
    """

    def __init__(self, raw_data: PlaceData) -> None:
        """Initialize a Place object.

        Args:
            raw_data: A dictionary representing the JSON response from 'places' REST API
                request. The structure is described by the PlaceData class.
        """
        self.raw_data = raw_data

    def __repr__(self) -> str:
        """Return string representation of this class.

        Returns:
            A string to represent the instance of the Place class using the name,
            country and admin area of the location.

            Example: <Place(name=Montréal, country=FR, admin=Languedoc-Roussillon)>
        """
        return "<{}(name={}, country={}, admin={})>".format(
            self.__class__.__name__, self.name, self.country, self.admin
        )

    def __str__(self) -> str:
        """Provide an easy way to identify the Place.

        Returns:
            A string to represent a Place instance with city name, Region name,
            department ID and the country name.

            For Examples:
                `Marseille - Provence-Alpes-Côte d'Azur (13) - FR`
                or `Montréal - Quebec - CA`
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
        """Return the admin of the place."""
        return self.raw_data.get("admin")

    @property
    def admin2(self) -> Optional[str]:
        """Return the admin2 of the place."""
        return self.raw_data.get("admin2")

    @property
    def postal_code(self) -> Optional[str]:
        """Return the postal code of the place."""
        return self.raw_data.get("postCode")
