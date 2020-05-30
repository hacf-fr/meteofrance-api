# -*- coding: utf-8 -*-
"""
Meteo France weather forecast python API. Rain class.
"""

from datetime import datetime

from pytz import timezone, utc

from .auth import Auth


class Rain(object):
    def __init__(self, raw_data: dict):
        """Initialize a Rain object."""
        self.raw_data = raw_data

    @property
    def position(self) -> dict:
        """Return the position information of the rain forecast."""
        return self.raw_data["position"]

    @property
    def updated_on(self) -> int:
        """Return the update timestamp of the rain forecast."""
        return self.raw_data["updated_on"]

    @property
    def forecast(self) -> list:
        """Return the rain forecast."""
        return self.raw_data["forecast"]

    @property
    def quality(self) -> int:
        """Return the quality of the rain forecast."""
        # TODO: don't know yet what is the usage
        return self.raw_data["quality"]

    def next_rain_date_locale(self) -> datetime:
        """Helper returning the date of the next rain in the Place timezone"""
        # search first cadran with rain
        next_rain = next(
            (cadran for cadran in self.forecast if cadran["rain"] > 1), None
        )

        if next_rain is not None:
            # get the time stamp of the first cadran with rain
            next_rain_timestamp = next_rain["dt"]
            # convert it in datetime with UTC timezone
            next_rain_dt_utc = utc.localize(
                datetime.utcfromtimestamp(next_rain_timestamp)
            )
            # convert datetime to Place timezone
            local_timezone = timezone(self.position["timezone"])
            next_rain_dt_local = next_rain_dt_utc.astimezone(local_timezone)
        else:
            next_rain_dt_local = None

        return next_rain_dt_local
