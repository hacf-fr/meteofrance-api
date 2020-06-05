# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API."""

from typing import Any

from requests import Response, Session

from .const import METEOFRANCE_API_TOKEN, METEOFRANCE_API_URL, METEOFRANCE_WS_API_URL


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, host: str, websession: Session = None, access_token: str = None):
        """Initialize the auth."""
        self.host = host
        self.websession = websession or Session()
        self.access_token = access_token or METEOFRANCE_API_TOKEN

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make a request."""
        params_inputs = kwargs.pop("params", None)

        params: dict = {"token": self.access_token}
        if params_inputs:
            params.update(params_inputs)

        response = self.websession.request(
            method, f"{self.host}/{path}", **kwargs, params=params
        )
        response.raise_for_status()

        return response


class MeteoFranceAuth(Auth):
    """Auth for Météo-France webservice."""

    # TODO: convert to class method
    def __init__(self):
        """Initialize the Météo-France webservice."""
        super().__init__(METEOFRANCE_API_URL)


class MeteoFranceWSAuth(Auth):
    """Auth for Météo-France WS."""

    # TODO: convert to class method
    def __init__(self):
        """Initialize the Météo-France WS."""
        super().__init__(METEOFRANCE_WS_API_URL)
