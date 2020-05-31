# -*- coding: utf-8 -*-
"""Meteo France weather forecast python API. Place class."""


class Place(object):
    """Class to access the results of 'places' API command."""

    def __init__(self, raw_data: dict):
        """Initialize a Place object."""
        self.raw_data = raw_data

    def __repr__(self):
        """Return string representation of this class."""
        return "<{}(name={}, country={}, admin={})>".format(
            self.__class__.__name__, self.name, self.country, self.admin
        )

    @property
    def insee(self) -> str:
        """Return the INSEE ID of the place."""
        return self.raw_data["insee"]

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
        """Return the country of the place."""
        return self.raw_data["country"]

    @property
    def admin(self) -> str:
        """Return the admin of the place.

        Seems to be the department in text ex: "Gers".
        """
        return self.raw_data["admin"]

    @property
    def admin2(self) -> str:
        """Return the admin2 of the place.

        Seems to be the department in numbers "32".
        """
        return self.raw_data["admin2"]

    @property
    def postcode(self) -> str:
        """Return the postcode of the place."""
        return self.raw_data["postCode"]

    def pretty_print(self) -> str:
        """Provide an easy way to identify the Place.

        examples: `Toulouse - (31)` or `Montréal - (Quebec)`
        """
        if self.country == "FR":
            pretty_str = "{} - ({})".format(self.name, self.admin2)
        else:
            pretty_str = "{} - ({})".format(self.name, self.admin)

        return pretty_str
