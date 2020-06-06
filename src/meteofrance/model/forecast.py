# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. Forecast class."""

from datetime import datetime

from pytz import timezone, utc


class Forecast:
    """Class to access the results of a `forecast` API command."""

    def __init__(self, raw_data: dict):
        """Initialize a Forecast object."""
        self.raw_data = raw_data

    @property
    def position(self) -> dict:
        """Return the position information of the forecast."""
        return self.raw_data["position"]

    @property
    def updated_on(self) -> int:
        """Return the update timestamp of the forecast."""
        return self.raw_data["updated_on"]

    @property
    def daily_forecast(self) -> list:
        """Return the daily forecast for the following days."""
        return self.raw_data["daily_forecast"]

    @property
    def forecast(self) -> list:
        """Return the hourly forecast."""
        return self.raw_data["forecast"]

    @property
    def probability_forecast(self) -> list:
        """Return the wheather event forecast."""
        return self.raw_data["probability_forecast"]

    @property
    def today_forecast(self) -> dict:
        """Return the forecast for today."""
        return self.daily_forecast[0]

    @property
    def nearest_forecast(self) -> dict:
        """Return the nearest hourly forecast."""
        now_timestamp = datetime.utcnow().timestamp()
        sorted_forecast = sorted(
            self.forecast, key=lambda x: abs(x["dt"] - now_timestamp)
        )
        return sorted_forecast[0]

    @property
    def current_forecast(self) -> dict:
        """Return the forecast of the current hour."""
        current_hour_timestamp = (
            datetime.utcnow().replace(minute=0, second=0, microsecond=0).timestamp()
        )
        return next(
            (x for x in self.forecast if x["dt"] == current_hour_timestamp),
            None,
        )

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert timestamp in datetime (Helper).

        The timezone corresponding to the forecast location is used.
        """
        # convert timestamp in datetime with UTC timezone
        dt_utc = utc.localize(datetime.utcfromtimestamp(timestamp))
        # convert datetime to Place timezone
        local_timezone = timezone(self.position["timezone"])
        return dt_utc.astimezone(local_timezone)
