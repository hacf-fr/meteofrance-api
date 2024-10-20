"""Météo-France models for the REST API."""

from .dictionary import WarningDictionary
from .forecast import Forecast
from .observation import Observation
from .picture_of_the_day import PictureOfTheDay
from .place import Place
from .rain import Rain
from .warning import CurrentPhenomenons
from .warning import Full


__all__ = [
    "Forecast",
    "Observation",
    "Place",
    "PictureOfTheDay",
    "Rain",
    "CurrentPhenomenons",
    "Full",
    "WarningDictionary",
]
