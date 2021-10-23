# -*- coding: utf-8 -*-
"""Client for the Météo-France REST API."""
from typing import List
from typing import Optional

from .const import COASTAL_DEPARTMENT_LIST
from .const import METEOFRANCE_API_TOKEN
from .const import METEOFRANCE_API_URL
from .model import CurrentPhenomenons
from .model import Forecast
from .model import Full
from .model import PictureOfTheDay
from .model import Place
from .model import Rain
from .session import MeteoFranceSession

# TODO: http://webservice.meteofrance.com/observation
# TODO: investigate bulletincote, montagne, etc...
#       http://ws.meteofrance.com/ws//getDetail/france/330630.json
# TODO: add protection for warning if domain not valid
# TODO: strategy for HTTP errors
# TODO: next rain in minute. Necessary ?
# TODO: forecast/metadata from ID to get gps ?


class MeteoFranceClient:
    """Proxy to the Météo-France REST API.

    You will find methods and helpers to request weather forecast, rain forecast and
    weather alert bulletin.
    """

    def __init__(self, access_token: Optional[str] = None) -> None:
        """Initialize the API and store the auth so we can make requests.

        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        self.session = MeteoFranceSession(access_token)

    #
    # Place
    #
    def search_places(
        self,
        search_query: str,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
    ) -> List[Place]:
        """Search the places (cities) linked to a query by name.

        You can add GPS coordinates in parameter to search places arround a given
        location.

        Args:
            search_query: A complete name, only a part of a name or a postal code (for
                France only) corresponding to a city in the world.
            latitude: Optional; Latitude in degree of a reference point to order
                results. The nearest places first.
            longitude: Optional; Longitude in degree of a reference point to order
                results. The nearest places first.

        Returns:
            A list of places (Place instance) corresponding to the query.
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
        self,
        latitude: float,
        longitude: float,
        language: str = "fr",
    ) -> Forecast:
        """Retrieve the weather forecast for a given GPS location.

        Results can be fetched in french or english according to the language parameter.

        Args:
            latitude: Latitude in degree of the GPS point corresponding to the weather
                forecast.
            longitude: Longitude in degree of the GPS point corresponding to the weather
                forecast.
            language: Optional; If language is equal "fr" (default value) results will
                be in French. All other value will give results in English.

        Returns:
            A Forecast intance representing the hourly and daily weather forecast.
        """
        # TODO: add possibility to request forecast from id

        # Send the API request
        resp = self.session.request(
            "get",
            "forecast",
            params={"lat": latitude, "lon": longitude, "lang": language},
        )
        return Forecast(resp.json())

    def get_forecast_for_place(
        self,
        place: Place,
        language: str = "fr",
    ) -> Forecast:
        """Retrieve the weather forecast for a given Place instance.

        Results can be fetched in french or english according to the language parameter.

        Args:
            place: Place class instance corresponding to a location.
            language: Optional; If language is equal "fr" (default value) results will
                be in French. All other value will give results in English.

        Returns:
            A Forecast intance representing the hourly and daily weather forecast.
        """
        return self.get_forecast(place.latitude, place.longitude, language)

    #
    # Rain
    #
    def get_rain(self, latitude: float, longitude: float, language: str = "fr") -> Rain:
        """Retrieve the next 1 hour rain forecast for a given GPS the location.

        Results can be fetched in french or english according to the language parameter.

        Args:
            latitude: Latitude in degree of the GPS point corresponding to the rain
                forecast.
            longitude: Longitude in degree of the GPS point corresponding to the rain
                forecast.
            language: Optional; If language is equal "fr" (default value) results will
                be in French. All other value will give results in English.

        Returns:
            A Rain instance representing the next hour rain forecast.
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

        Args:
            domain: could be `france` or any metropolitan France department numbers on
                two digits. For some departments you can access an additional bulletin
                for coastal phenomenoms. To access it add `10` after the domain id
                (example: `1310`).
            depth: Optional; To be used with domain = 'france'. With depth = 0 the
                results will show only natinal sum up of the weather alerts. If
                depth = 1, you will have in addition, the bulletin for all metropolitan
                France department and Andorre
            with_costal_bulletin: Optional; If set to True (default is False), you can
                get the basic bulletin and coastal bulletin merged.

        Returns:
            A warning.CurrentPhenomenons instance representing the weather alert
            bulletin.
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
        """Retrieve a complete bulletin of the weather phenomenons for a given domain.

        For a given domain we can access the maximum alert, a timelaps of the alert
        evolution for the next 24 hours, a list of alerts and other metadatas.

        Args:
            domain: could be `france` or any metropolitan France department numbers on
                two digits. For some departments you can access an additional bulletin
                for coastal phenomenoms. To access it add `10` after the domain id
                (example: `1310`).
            with_costal_bulletin: Optional; If set to True (default is False), you can
                get the basic bulletin and coastal bulletin merged.

        Returns:
            A warning.Full instance representing the complete weather alert bulletin.
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
                    "get",
                    "warning/full",
                    params={"domain": domain + "10"},
                )
                full_phenomenoms.merge_with_coastal_phenomenons(Full(resp.json()))

        return full_phenomenoms

    def get_warning_thumbnail(self, domain: str = "france") -> str:
        """Retrieve the thumbnail URL of the weather phenomenoms or alerts map.

        Args:
            domain: could be `france` or any metropolitan France department numbers on
                two digits.

        Returns:
            The URL of the thumbnail representing the weather alert status.
        """
        # Return directly the URL of the gif image
        return (
            f"{METEOFRANCE_API_URL}/warning/thumbnail?&token={METEOFRANCE_API_TOKEN}"
            f"&domain={domain}"
        )

    #
    # Picture of the day
    #
    def get_picture_of_the_day(self, domain: str = "france") -> PictureOfTheDay:
        """Retrieve the picture of the day image URL & description.

        Args:
            domain: could be `france`

        Returns:
            PictureOfTheDay instance with the URL and the description of the picture of
            the day.
        """
        # Send the API request
        # TODO: check if other value of domain are usable

        resp = self.session.request(
            "get",
            "v2/report",
            params={
                "domain": domain,
                "report_type": "observation",
                "report_subtype": "image du jour",
                "format": "txt",
            },
        )

        image_url = (
            f"{METEOFRANCE_API_URL}/v2/report"
            f"?domain={domain}"
            f"&report_type=observation&report_subtype=image%20du%20jour&format=jpg"
            f"&token={METEOFRANCE_API_TOKEN}"
        )

        return PictureOfTheDay({"image_url": image_url, "description": resp.text})
