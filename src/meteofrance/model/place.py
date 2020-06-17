# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. Place class."""


class Place:
    """Class to access the results of 'places' API command."""

    def __init__(self, raw_data: dict):
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
    def insee(self) -> str:
        """Return the INSEE ID of the place."""
        return self.raw_data.get("insee")

    @property
    def name(self) -> str:
        """Return the name of the place."""
        return self.raw_data["name"]

    @property
    def latitude(self) -> str:
        """Return the latitude of the place."""
        return self.raw_data["lat"]

    @property
    def longitude(self) -> str:
        """Return the longitude of the place."""
        return self.raw_data["lon"]

    @property
    def country(self) -> str:
        """Return the country code of the place."""
        return self.raw_data["country"]

    @property
    def admin(self) -> str:
        """Return the admin of the place.

        Seems to be the department in text ex: "Gers".
        """
        return self.raw_data.get("admin")

    @property
    def admin2(self) -> str:
        """Return the admin2 of the place.

        Seems to be the department in numbers "32".
        """
        return self.raw_data.get("admin2")

    @property
    def postal_code(self) -> str:
        """Return the postal code of the place."""
        return self.raw_data.get("postCode")
