# -*- coding: utf-8 -*-
"""Weather forecast Python model for the Météo-France REST API."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pytz import utc

from meteofrance_api.helpers import timestamp_to_dateime_with_locale_tz


@dataclass
class Forecast:
    """Class to access the results of a `forecast` API request.

    Attributes:
        position: A dictionary with metadata about the position of the forecast place.
        updated_on: A timestamp as int corresponding to the latest update date.
        daily_forecast: A list of dictionaries to describe the daily forecast for the
            next 15 days.
        forecast: A list of dictionaries to describe the hourly forecast for the next
            days.
        probability_forecast: A list of dictionaries to describe the event probability
            forecast (rain, snow, freezing) for next 10 days.
        today_forecast: A dictionary corresponding to the daily forecast for the current
        day.
        nearest_forecast: A dictionary corresponding to the nearest hourly forecast.
        current_forecast: A dictionary corresponding to the hourly forecast for the
            current hour.
    """

    geometry: Dict[str, Any]
    update_time: int
    type: str
    properties: Dict[str, Optional[Any]]

    # @property
    # def daily_forecast(self) -> List[Dict[str, Any]]:
    #     """Return the daily forecast for the following days."""
    #     return self.raw_data["daily_forecast"]

    # @property
    # def forecast(self) -> List[Dict[str, Any]]:
    #     """Return the hourly forecast."""
    #     return self.raw_data["forecast"]

    @property
    def probability_forecast(self) -> List[Dict[str, Any]]:
        """Return the wheather event forecast."""
        return self.properties.get("probability_forecast", [])

    @property
    def today_forecast(self) -> Dict[str, Any]:
        """Return the forecast for today."""
        return self.properties["daily_forecast"][0]

    @property
    def nearest_forecast(self) -> Dict[str, Any]:
        """Return the nearest hourly forecast."""
        # get timestamp for current time
        now_timestamp = int(utc.localize(datetime.utcnow()).timestamp())
        # sort list of forecast by distance between current timestamp and
        # forecast timestamp
        sorted_forecast = sorted(
            self.properties["forecast"],
            key=lambda x: abs(x["time"] - now_timestamp),  # type: ignore[no-any-return]
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
        forecast_by_datetime = {
            item["time"]: item for item in self.properties["forecast"]
        }
        # Return the forecast corresponding to the timestamp of the current hour if
        # exists. If not exists, returns the nearest forecast (for not France countries)
        return forecast_by_datetime.get(current_hour_timestamp, self.nearest_forecast)

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert timestamp in datetime in the forecast location timezone (Helper).

        Args:
            timestamp: An integer to describe the UNIX timestamp.

        Returns:
            Datetime instance corresponding to the timestamp with the timezone of the
                forecast location.
        """
        return timestamp_to_dateime_with_locale_tz(
            timestamp, self.properties["timezone"]
        )
