# -*- coding: utf-8 -*-
"""Weather observation Python model for the Météo-France REST API."""
import sys
from datetime import datetime

if sys.version_info >= (3, 8):
	from typing import TypedDict  # pylint: disable=no-name-in-module
else:
	from typing_extensions import TypedDict


class ObservationDataPropertiesGridded(TypedDict, total=True):
	time: str
	T: float
	wind_speed: float
	wind_direction: int
	wind_icon: str
	weather_icon: str
	weather_description: str


class ObservationDataProperties(TypedDict, total=False):
	timezone: str
	gridded: ObservationDataPropertiesGridded


class ObservationData(TypedDict, total=False):
	"""Describing the data structure of the observation object returned by the REST API."""
	
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
		self.properties = raw_data.get('properties', dict())

	@property
	def timezone(self) -> str:
		"""Returns the observation timezone"""
		return self.properties.get('timezone')

	@property
	def _gridded(self) -> ObservationDataPropertiesGridded:
		"""Returns the observation gridded properties"""
		return self.properties.get('gridded', dict())

	@property
	def time_as_string(self) -> str:
		"""Returns the time at which the observation was made"""
		return self._gridded.get('time')

	@property
	def time_as_datetime(self) -> str:
		"""Returns the time at which the observation was made"""
		time = self.time_as_string
		return None if time is None else datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')

	@property
	def temperature(self) -> float:
		"""Returns the observed temperature (°C)"""
		return self._gridded.get('T')
	
	@property
	def wind_speed(self) -> float:
		"""Returns the observed wind speed (km/h)"""
		return self._gridded.get('wind_speed')
	
	@property
	def wind_direction(self) -> int:
		"""Returns the observed wind direction (°)"""
		return self._gridded.get('wind_direction')
	
	@property
	def wind_icon(self) -> str:
		"""Returns an icon ID illustrating the observed wind direction"""
		return self._gridded.get('wind_icon')
	
	@property
	def weather_icon(self) -> str:
		"""Returns an icon ID illustrating the observed weather condition"""
		return self._gridded.get('weather_icon')
	
	@property
	def weather_description(self) -> str:
		"""Returns a description of the observed weather condition"""
		return self._gridded.get('weather_description')
	
	def __repr__(self) -> str:
		"""Returns a stringified version of the object"""
		return f"Observation(timezone={self.timezone}, time={self.time}, temperature={self.temperature}°C, "\
			f"wind_speed={self.wind_speed} km/h, wind_direction={self.wind_direction}°, wind_icon={self.wind_icon}, "\
			f"weather_icon={self.weather_icon}, weather_description={self.weather_description}"
