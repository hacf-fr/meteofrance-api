# -*- coding: utf-8 -*-
"""Picture of the Day Python model for the Météo-France REST API."""
from dataclasses import dataclass


@dataclass
class PictureOfTheDay:
    """Class to access the results of a `ImageJour/last` REST API request.

    Attributes:
        image_url: A string corresponding to the picture of the day URL.
        descritpion: A string with the description of the picture of the day.
    """

    image_url: str  # noqa: N815
    description: str
