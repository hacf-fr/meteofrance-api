# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API."""

from requests import Response, Session

from .const import METEOFRANCE_API_TOKEN, METEOFRANCE_API_URL, METEOFRANCE_WS_API_URL


class MeteoFranceSession(Session):
    """Class to make authenticated requests."""

    host: str = METEOFRANCE_API_URL

    def __init__(self, access_token: str = None):
        """Initialize the auth."""
        self.access_token = access_token or METEOFRANCE_API_TOKEN
        Session.__init__(self)

    def request(self, method: str, path: str, **kwargs) -> Response:
        """Make a request."""
        params_inputs = kwargs.pop("params", None)

        params: dict = {"token": self.access_token}
        if params_inputs:
            params.update(params_inputs)

        response = super().request(
            method, f"{self.host}/{path}", **kwargs, params=params
        )
        response.raise_for_status()

        return response


class MeteoFranceWSSession(MeteoFranceSession):
    """Auth for Météo-France WS."""

    host: str = METEOFRANCE_WS_API_URL

    # TODO: convert to class method
    def __init__(self, access_token: str = None):
        """Initialize the Météo-France WS."""
        super().__init__(access_token)
