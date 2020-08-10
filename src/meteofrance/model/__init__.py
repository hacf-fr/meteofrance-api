"""Météo-France models for the REST API."""
from .forecast import Forecast
from .picture_of_the_day import PictureOfTheDay
from .place import Place
from .rain import Rain
from .warning import CurrentPhenomenons
from .warning import Full

__all__ = ["Forecast", "Place", "PictureOfTheDay", "Rain", "CurrentPhenomenons", "Full"]
