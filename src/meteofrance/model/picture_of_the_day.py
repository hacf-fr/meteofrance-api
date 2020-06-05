# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. PictureOfTheDay class."""


class PictureOfTheDay:
    """Class to access the results of a `ImageJour/last` API command."""

    def __init__(self, raw_data: dict):
        """Initialize a PictureOfTheDay object."""
        self.raw_data = raw_data["result"]

    @property
    def image_url(self) -> str:
        """Return the image URL of the picture of the day."""
        return self.raw_data["vignette"]

    @property
    def image_hd_url(self) -> str:
        """Return the image HD URL of the picture of the day."""
        return self.raw_data["imageHD"]

    @property
    def description(self) -> str:
        """Return the description of the picture of the day."""
        return self.raw_data["commentaire"]
