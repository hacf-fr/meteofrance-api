# -*- coding: utf-8 -*-
"""Meteo France weather forecast python API."""

from typing import Any

from requests import Response, Session

from .const import METEOFRANCE_API_TOKEN, METEOFRANCE_API_URL


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: Session, host: str, access_token: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self.access_token = access_token

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make a request."""
        params_inputs = kwargs.pop("params", None)

        params: dict = {"token": self.access_token}
        if params_inputs is not None:
            params.update(dict(params_inputs))

        return self.websession.request(
            method, f"{self.host}/{path}", **kwargs, params=params
        )


class AuthMeteofrance(Auth):
    """Generic Auth for meteofrance as token is static."""

    # TODO: convert to class method
    def __init__(self):
        """Initialize the standard for Meteo-France."""
        super().__init__(Session(), METEOFRANCE_API_URL, METEOFRANCE_API_TOKEN)
