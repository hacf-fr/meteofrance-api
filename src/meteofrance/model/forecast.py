# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. Forecast class."""
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import TypedDict

from pytz import utc

from meteofrance.helpers import timestamp_to_dateime_with_locale_tz


class ForecastData(TypedDict):
    """Describing the structure of the API returned forecast object."""

    position: Dict[str, Any]
    updated_on: int
    daily_forecast: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    probability_forecast: List[Dict[str, Any]]


class Forecast:
    """Class to access the results of a `forecast` API command."""

    def __init__(self, raw_data: ForecastData):
        """Initialize a Forecast object."""
        self.raw_data = raw_data

    @property
    def position(self) -> Dict[str, Any]:
        """Return the position information of the forecast."""
        return self.raw_data["position"]

    @property
    def updated_on(self) -> int:
        """Return the update timestamp of the forecast."""
        return self.raw_data["updated_on"]

    @property
    def daily_forecast(self) -> List[Dict[str, Any]]:
        """Return the daily forecast for the following days."""
        return self.raw_data["daily_forecast"]

    @property
    def forecast(self) -> List[Dict[str, Any]]:
        """Return the hourly forecast."""
        return self.raw_data["forecast"]

    @property
    def probability_forecast(self) -> List[Dict[str, Any]]:
        """Return the wheather event forecast."""
        return self.raw_data.get("probability_forecast", [])

    @property
    def today_forecast(self) -> Dict[str, Any]:
        """Return the forecast for today."""
        return self.daily_forecast[0]

    @property
    def nearest_forecast(self) -> Dict[str, Any]:
        """Return the nearest hourly forecast."""
        # get timestamp for current time
        now_timestamp = int(utc.localize(datetime.utcnow()).timestamp())
        # sort list of foerecast by distance between current timestamp and
        # forecast timestamp
        sorted_forecast = sorted(
            self.forecast, key=lambda x: abs(x["dt"] - now_timestamp)
        )
        return sorted_forecast[0]

    @property
    def current_forecast(self) -> Dict[str, Any]:
        """Return the forecast of the current hour."""
        # Get the timestamp for the current hour.
        current_hour_timestamp = int(
            utc.localize(
                datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            ).timestamp()
        )
        # create a dict using timestamp as keys
        forecast_by_datetime = {item["dt"]: item for item in self.forecast}
        # Return the forecast corresponding to the timestamp of the current hour if
        # exists. If not exists, returns the nearest forecast (not France countries)
        return forecast_by_datetime.get(current_hour_timestamp, self.nearest_forecast)

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert timestamp in datetime (Helper).

        The timezone corresponding to the forecast location is used.
        """
        return timestamp_to_dateime_with_locale_tz(timestamp, self.position["timezone"])
