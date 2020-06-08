# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API."""

from typing import List

from .const import COASTAL_DEPARTMENT_LIST, METEOFRANCE_API_TOKEN, METEOFRANCE_API_URL
from .model import CurrentPhenomenons, Forecast, Full, PictureOfTheDay, Place, Rain
from .session import MeteoFranceSession, MeteoFranceWSSession, MeteoNetSession

# TODO: http://webservice.meteofrance.com/observation
# TODO: investigate bulletincote, montagne, etc...
#       http://ws.meteofrance.com/ws//getDetail/france/330630.json
# TODO: add protection for warning if domain not valid
# TODO: strategy for HTTP errors
# TODO: next rain in minute. Necessary ?
# TODO: forecast/metadata from ID to get gps ?


class MeteoFranceClient:
    """Proxy to the Météo-France API.

    You will find methods and helpers to request weather forecast, rain forecast and
    weather alert bulletin.
    """

    def __init__(self, access_token: str = None):
        """Initialize the API and store the auth so we can make requests."""
        self.session = MeteoFranceSession(access_token)
        self.session_ws = MeteoFranceWSSession()
        self.session_net = MeteoNetSession()

    #
    # Place
    #
    def search_places(
        self, search_query: str, latitude: str = None, longitude: str = None
    ) -> List[Place]:
        """Return the places link to a search.

        You can add GPS coordinates in parameter to search places arround a given
        location.
        """
        # Construct the list of the GET parameters
        params = {"q": search_query}
        if latitude is not None:
            params["lat"] = latitude
        if longitude is not None:
            params["lon"] = longitude

        # Send the API resuest
        resp = self.session.request("get", "places", params=params)
        return [Place(place_data) for place_data in resp.json()]

    #
    # Forecast
    #
    def get_forecast(
        self, latitude: str, longitude: str, language: str = "fr",
    ) -> Forecast:
        """Return the weather forecast for a GPS location.

        Results can be fetched in french or english according to the language parameter.
        """
        # TODO: add possibility to request forecast from id

        # Send the API request
        resp = self.session.request(
            "get",
            "forecast",
            params={"lat": latitude, "lon": longitude, "lang": language},
        )
        return Forecast(resp.json())

    def get_forecast_for_place(self, place: Place, language: str = "fr",) -> Forecast:
        """Return the weather forecast for a Place.

        Results can be fetched in french or english according to the language parameter.
        """
        return self.get_forecast(place.latitude, place.longitude, language)

    #
    # Rain
    #
    def get_rain(self, latitude: str, longitude: str, language: str = "fr") -> Rain:
        """Return the next 1 hour rain forecast for a GPS the location.

        Results can be fetched in french or english according to the language parameter.
        """
        # TODO: add protection if no rain forecast for this position

        # Send the API request
        resp = self.session.request(
            "get", "rain", params={"lat": latitude, "lon": longitude, "lang": language}
        )
        return Rain(resp.json())

    #
    # Warning
    #
    def get_warning_current_phenomenoms(
        self, domain: str, depth: int = 0, with_costal_bulletin: bool = False
    ) -> CurrentPhenomenons:
        """Return the current weather phenomenoms (or alerts) for a given domain.

        domain: could be `france` or any department numbers on two digits.
        For some departments you ca access an additional bulletin for coastal
        phenomenoms.
        To access it add `10` after the domain id (example: `1310`).

        with_costal_bulletin: If set to True, you can get the basic bulletin and
        coastal bulletin merged.

        depth: use 1 with `france` domain to have all sub location phenomenoms.
        """
        # Send the API request
        resp = self.session.request(
            "get",
            "warning/currentphenomenons",
            params={"domain": domain, "depth": depth},
        )

        # Create object with API response
        phenomenoms = CurrentPhenomenons(resp.json())

        # if user ask to have the coastal bulletin merged
        if with_costal_bulletin:
            if domain in COASTAL_DEPARTMENT_LIST:
                resp = self.session.request(
                    "get",
                    "warning/currentphenomenons",
                    params={"domain": domain + "10"},
                )
                phenomenoms.merge_with_coastal_phenomenons(
                    CurrentPhenomenons(resp.json())
                )

        return phenomenoms

    def get_warning_full(self, domain: str, with_costal_bulletin: bool = False) -> Full:
        """Return a complete bulletin of the weather phenomenons for a given domain.

        For a given domain we can access the maximum alert, a timelaps of the alert
        evolution for
        the next 24 hours, a list of alerts and other metadatas.

        domain: could be `france` or any department numbers on two digits.
        For some department you can access an additional bulletin for coastal
        phenomenoms.
        To access it add `10` after the domain id (example: `1310`).

        with_costal_bulletin: If set to True, you can get the basic bulletin and
        coastal bulletin merged.
        """
        # TODO: add formatDate parameter

        # Send the API request
        resp = self.session.request("get", "warning/full", params={"domain": domain})

        # Create object with API response
        full_phenomenoms = Full(resp.json())

        # if user ask to have the coastal bulletin merged
        if with_costal_bulletin:
            if domain in COASTAL_DEPARTMENT_LIST:
                resp = self.session.request(
                    "get", "warning/full", params={"domain": domain + "10"},
                )
                full_phenomenoms.merge_with_coastal_phenomenons(Full(resp.json()))

        return full_phenomenoms

    def get_warning_thumbnail(self, domain: str = "france") -> str:
        """Return the thumbnail of the weather phenomenoms or alerts map."""
        # Return directly the URL of the gif image
        return (
            f"{METEOFRANCE_API_URL}/warning/thumbnail?&token={METEOFRANCE_API_TOKEN}"
            f"&domain={domain}"
        )

    #
    # Picture of the day
    #
    def get_picture_of_the_day(self) -> PictureOfTheDay:
        """Return the picture of the day image URL & description."""
        resp = self.session_net.request("get", "ImageJour/last.txt")
        return PictureOfTheDay(resp.json())
