"""Weather forecast Python model for the Météo-France REST API."""

from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields as dc_fields
from datetime import datetime
from datetime import timezone

from pytz import timezone as pytz_timezone

from meteofrance_api.helpers import timestamp_to_datetime_with_locale_tz


@dataclass
class ForecastPosition:
    """Metadata about the forecast location."""

    altitude: int | None = None
    name: str | None = None
    country: str | None = None
    french_department: str | None = None
    rain_product_available: int | None = None
    timezone: str | None = None
    insee: str | None = None
    bulletin_cote: int | None = None
    lat: float | None = None
    lon: float | None = None

    @classmethod
    def from_api_response(cls, properties: dict, coords: list) -> "ForecastPosition":
        known = {f.name for f in dc_fields(cls)}
        data = {k: v for k, v in properties.items() if k in known}
        data["lat"] = coords[1]
        data["lon"] = coords[0]
        return cls(**data)


@dataclass
class DailyForecast:
    """One day of forecast data."""

    time: str
    T_min: float | None = None
    T_max: float | None = None
    T_sea: float | None = None
    relative_humidity_min: int | None = None
    relative_humidity_max: int | None = None
    total_precipitation_24h: float | None = None
    uv_index: int | None = None
    daily_weather_icon: str | None = None
    daily_weather_description: str | None = None
    sunrise_time: str | None = None
    sunset_time: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "DailyForecast":
        known = {f.name for f in dc_fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class HourlyForecast:
    """One time-step of hourly (or 3h/6h) forecast data."""

    time: str
    T: float | None = None
    T_windchill: float | None = None
    relative_humidity: int | None = None
    P_sea: float | None = None
    wind_speed: int | None = None
    wind_speed_gust: int | None = None
    wind_direction: int | None = None
    wind_icon: str | None = None
    rain_1h: float | None = None
    rain_3h: float | None = None
    rain_6h: float | None = None
    rain_12h: float | None = None
    rain_24h: float | None = None
    snow_1h: float | None = None
    snow_3h: float | None = None
    snow_6h: float | None = None
    snow_12h: float | None = None
    snow_24h: float | None = None
    iso0: int | None = None
    rain_snow_limit: str | int | None = None
    total_cloud_cover: int | None = None
    weather_icon: str | None = None
    weather_description: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "HourlyForecast":
        known = {f.name for f in dc_fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class ProbabilityForecast:
    """Hazard probabilities for one time-step (France only)."""

    time: str
    rain_hazard_3h: int | None = None
    rain_hazard_6h: int | None = None
    snow_hazard_3h: int | None = None
    snow_hazard_6h: int | None = None
    freezing_hazard: int | None = None
    storm_hazard: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProbabilityForecast":
        known = {f.name for f in dc_fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class Forecast:
    """Météo-France v2 forecast data.

    Attributes:
        position: Metadata about the forecast location.
        updated_on: Unix timestamp of the latest model run.
        daily_forecast: Daily forecast for the next 15 days.
        forecast: Hourly (then 3h/6h) forecast entries.
        probability_forecast: Rain/snow/freezing hazard probabilities (France only).
    """

    position: ForecastPosition
    updated_on: int
    daily_forecast: list[DailyForecast]
    forecast: list[HourlyForecast]
    probability_forecast: list[ProbabilityForecast] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, raw_data: dict) -> "Forecast":
        """Build a Forecast from a v2/forecast API response dict."""
        properties = raw_data["properties"]
        coords = raw_data["geometry"]["coordinates"]
        dt = datetime.fromisoformat(raw_data["update_time"].replace("Z", "+00:00"))
        return cls(
            position=ForecastPosition.from_api_response(properties, coords),
            updated_on=int(dt.timestamp()),
            daily_forecast=[DailyForecast.from_dict(e) for e in properties["daily_forecast"]],
            forecast=[HourlyForecast.from_dict(e) for e in properties["forecast"]],
            probability_forecast=[
                ProbabilityForecast.from_dict(e)
                for e in properties.get("probability_forecast", [])
            ],
        )

    @property
    def today_forecast(self) -> DailyForecast:
        """Return the forecast for today."""
        return self.daily_forecast[0]

    @property
    def nearest_forecast(self) -> HourlyForecast:
        """Return the hourly forecast entry closest to the current time."""
        now = datetime.now(timezone.utc)
        return min(
            self.forecast,
            key=lambda x: abs(
                (datetime.fromisoformat(x.time.replace("Z", "+00:00")) - now).total_seconds()
            ),
        )

    @property
    def current_forecast(self) -> HourlyForecast:
        """Return the forecast for the current hour, or nearest if unavailable."""
        now = datetime.now(timezone.utc)
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        for item in self.forecast:
            if datetime.fromisoformat(item.time.replace("Z", "+00:00")) == current_hour:
                return item
        return self.nearest_forecast

    def timestamp_to_locale_time(self, timestamp: int) -> datetime:
        """Convert a Unix timestamp to a datetime in the forecast location timezone."""
        return timestamp_to_datetime_with_locale_tz(timestamp, self.position.timezone)

    def iso_to_locale_time(self, iso_string: str) -> datetime:
        """Convert an ISO 8601 string to a datetime in the forecast location timezone."""
        dt_utc = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt_utc.astimezone(pytz_timezone(self.position.timezone))
