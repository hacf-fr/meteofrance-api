# -*- coding: utf-8 -*-
"""Weather observation Python model for the Météo-France REST API."""
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict
	
class Observation:
	def __init__(self, data: TypedDict):
		properties = data['properties']['gridded']
		self.time = properties['time']
		self.temp = properties['T']
		self.wind_speed = properties['wind_speed']
		self.wind_direction = properties['wind_direction']
		self.wind_icon = properties['wind_icon']
		self.weather_icon = properties['weather_icon']
		self.weather_description = properties['weather_description']
	
	def __repr__(self):
		return f"Observation(time={self.time}, temp={self.temp}, wind_speed={self.wind_speed}, "\
			f"wind_direction={self.wind_direction}, wind_icon={self.wind_icon}, "\
			f"weather_icon={self.weather_icon}, weather_description={self.weather_description}"
