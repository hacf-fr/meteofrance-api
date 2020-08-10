# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API. Rain class."""
import sys
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from meteofrance.helpers import timestamp_to_dateime_with_locale_tz

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict


class RainData(TypedDict):
    """Describing the structure of the API returned rain object."""

    position: Dict[str, Any]
    updated_on: int
    forecast: List[Dict[str, Any]]
    quality: int


class Rain:
    """Class to access the results of 'rain' API command."""

    def __init__(self, raw_data: RainData):
        """Initialize a Rain object."""
        self.raw_data = raw_data

    @property
    def position(self) -> Dict[str, Any]:
        """Return the position information of the rain forecast."""
        return self.raw_data["position"]

    @property
    def updated_on(self) -> int:
        """Return the update timestamp of the rain forecast."""
        return self.raw_data["updated_on"]

    @property
    def forecast(self) -> List[Dict[str, Any]]:
        """Return the rain forecast."""
        return self.raw_data["forecast"]

    @property
    def quality(self) -> int:
        """Return the quality of the rain forecast."""
        # TODO: don't know yet what is the usage
        return self.raw_data["quality"]

    def next_rain_date_locale(self) -> Optional[datetime]:
        """Return the date of the next rain in the Place timezone (Helper)."""
        # search first cadran with rain
        next_rain = next(
            (cadran for cadran in self.forecast if cadran["rain"] > 1), None
        )

        next_rain_dt_local: Optional[datetime] = None
        if next_rain is not None:
            # get the time stamp of the first cadran with rain
            next_rain_timestamp = next_rain["dt"]
            # convert timestamp in datetime with local timezone
            next_rain_dt_local = timestamp_to_dateime_with_locale_tz(
                next_rain_timestamp, self.position["timezone"]
            )

        return next_rain_dt_local

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert timestamp in datetime (Helper).

        The timezone corresponding to the forecast location is used.
        """
        return timestamp_to_dateime_with_locale_tz(timestamp, self.position["timezone"])
