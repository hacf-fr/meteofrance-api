# -*- coding: utf-8 -*-
"""Rain in the next hour Python model for the Météo-France REST API."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

from meteofrance_api.helpers import timestamp_to_dateime_with_locale_tz


@dataclass
class Rain:
    """Class to access the results of 'rain' REST API request.

    Attributes:
        position: A dictionary with metadata about the position of the forecast place.
        updated_on:  A timestamp as int corresponding to the latest update date.
        forecast: A list of dictionaries to describe the following next hour rain
            forecast.
        quality: An integer. Don't know yet the usage.
    """

    geometry: Dict[str, Any]
    update_time: int
    type: str
    properties: Dict[str, Any]

    def next_rain_date_locale(self) -> Optional[datetime]:
        """Estimate the date of the next rain in the Place timezone (Helper).

        Returns:
            A datetime instance representing the date estimation of the next rain within
            the next hour.
            If no rain is expected in the following hour 'None' is returned.

            The datetime use the location timezone.
        """
        # search first cadran with rain
        next_rain = next(
            (
                cadran
                for cadran in self.properties["forecast"]
                if cadran["rain_intensity"] > 1
            ),
            None,
        )

        next_rain_dt_local: Optional[datetime] = None
        if next_rain is not None:
            # get the time stamp of the first cadran with rain
            next_rain_timestamp = next_rain["time"]
            # convert timestamp in datetime with local timezone
            next_rain_dt_local = timestamp_to_dateime_with_locale_tz(
                next_rain_timestamp, self.properties["timezone"]
            )

        return next_rain_dt_local

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert timestamp in datetime with rain forecast location timezone (Helper).

        Args:
            timestamp: An integer representing the UNIX timestamp.

        Returns:
            A datetime instance corresponding to the timestamp with the timezone of the
                rain forecast location.
        """
        return timestamp_to_dateime_with_locale_tz(
            timestamp, self.properties["timezone"]
        )
