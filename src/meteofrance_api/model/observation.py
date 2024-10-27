"""Weather observation Python model for the Météo-France REST API."""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import TypedDict


class ObservationDataPropertiesGridded(TypedDict, total=False):
    """Data structure of the observation gridded properties object from the REST API."""

    time: str
    T: float
    wind_speed: float
    wind_direction: int
    wind_icon: str
    weather_icon: str
    weather_description: str


class ObservationDataProperties(TypedDict, total=False):
    """Data structure of the observation properties object from the REST API."""

    timezone: str
    gridded: ObservationDataPropertiesGridded


class ObservationData(TypedDict, total=False):
    """Data structure of the observation object from the REST API."""

    update_time: str
    geometry: Dict[str, Any]
    type: str
    properties: ObservationDataProperties


class Observation:
    """Class to access the results of an `observation` API request.

    Attributes:
            timezone: The observation timezone
            time: The time at which the observation was made
            temperature: The observed temperature (°C)
            wind_speed: The observed wind speed (km/h)
            wind_direction: The observed wind direction (°)
            wind_icon: An icon ID illustrating the observed wind direction
            weather_icon: An icon ID illustrating the observed weather condition
            weather_description: A description of the observed weather condition
    """

    def __init__(self, raw_data: ObservationData) -> None:
        """Initialize an Observation object.

        Args:
                raw_data: A dictionary representing the JSON response from 'observation' REST
                        API request. The structure is described by the ObservationData class.
        """
        self.properties = raw_data.get("properties", {})

    @property
    def timezone(self) -> Optional[str]:
        """Returns the observation timezone."""
        return self.properties.get("timezone")

    @property
    def _gridded(self) -> ObservationDataPropertiesGridded:
        """Returns the observation gridded properties."""
        return self.properties.get("gridded", {})

    @property
    def time_as_string(self) -> Optional[str]:
        """Returns the time at which the observation was made."""
        return self._gridded.get("time")

    @property
    def time_as_datetime(self) -> Optional[datetime]:
        """Returns the time at which the observation was made."""
        time = self.time_as_string
        return (
            None if time is None else datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
        )

    @property
    def temperature(self) -> Optional[float]:
        """Returns the observed temp (°C)."""
        return self._gridded.get("T")

    @property
    def wind_speed(self) -> Optional[float]:
        """Returns the observed wind speed (km/h)."""
        return self._gridded.get("wind_speed")

    @property
    def wind_direction(self) -> Optional[int]:
        """Returns the observed wind direction (°)."""
        return self._gridded.get("wind_direction")

    @property
    def wind_icon(self) -> Optional[str]:
        """Returns an icon ID illustrating the observed wind direction."""
        return self._gridded.get("wind_icon")

    @property
    def weather_icon(self) -> Optional[str]:
        """Returns an icon ID illustrating the observed weather condition."""
        return self._gridded.get("weather_icon")

    @property
    def weather_description(self) -> Optional[str]:
        """Returns a description of the observed weather condition."""
        return self._gridded.get("weather_description")

    def __repr__(self) -> str:
        """Returns a stringified version of the object."""
        return (
            f"Observation("
            f"	timezone={self.timezone},"
            f"	time={self.time_as_string},"
            f"	temperature={self.temperature}°C,"
            f"	wind_speed={self.wind_speed} km/h,"
            f"	wind_direction={self.wind_direction}°,"
            f"	wind_icon={self.wind_icon},"
            f"	weather_icon={self.weather_icon},"
            f"	weather_description={self.weather_description}"
            ")"
        )
