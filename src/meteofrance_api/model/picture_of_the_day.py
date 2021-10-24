# -*- coding: utf-8 -*-
"""Picture of the Day Python model for the Météo-France REST API."""
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict


class PictureOfTheDayData(TypedDict):
    """Describing the data structure of ImageJour object."""

    image_url: str  # noqa: N815
    description: str


class PictureOfTheDay:
    """Class to access the results of a `ImageJour/last` REST API request.

    Attributes:
        image_url: A string corresponding to the picture of the day URL.
        image_hd_url: A string corresponding to the URL for the HD version of the
            picture of the day.
        descritpion: A string with the description of the picture of the day.
    """

    def __init__(self, raw_data: PictureOfTheDayData) -> None:
        """Initialize a PictureOfTheDay object.

        Args:
            raw_data: A dictionary representing the JSON response from 'ImageJour/last'
                REST API request. The structure is described by the PictureOfTheDayData
                class.
        """
        self.raw_data = raw_data

    @property
    def image_url(self) -> str:
        """Return the image URL of the picture of the day."""
        return self.raw_data["image_url"]

    @property
    def description(self) -> str:
        """Return the description of the picture of the day."""
        return self.raw_data["description"]
