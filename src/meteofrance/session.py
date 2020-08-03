# -*- coding: utf-8 -*-
"""Météo-France weather forecast python API."""
from typing import Any
from typing import Optional

from requests import Response
from requests import Session

from .const import METEOFRANCE_API_TOKEN
from .const import METEOFRANCE_API_URL
from .const import METEOFRANCE_WS_API_URL
from .const import METEONET_API_URL


class MeteoFranceSession(Session):
    """Session for Météo-France."""

    host: str = METEOFRANCE_API_URL

    def __init__(self, access_token: Optional[str] = None):
        """Initialize the auth."""
        self.access_token = access_token or METEOFRANCE_API_TOKEN
        Session.__init__(self)

    def request(  # type: ignore
        self, method: str, path: str, *args: Any, **kwargs: Any
    ) -> Response:
        """Make a request."""
        params_inputs = kwargs.pop("params", None)

        params = {"token": self.access_token}
        if params_inputs:
            params.update(params_inputs)

        kwargs["params"] = params
        response = super().request(method, f"{self.host}/{path}", *args, **kwargs)
        response.raise_for_status()

        return response


class MeteoFranceWSSession(MeteoFranceSession):
    """Session for Météo-France WS."""

    host: str = METEOFRANCE_WS_API_URL

    # TODO: convert to class method
    def __init__(self, access_token: Optional[str] = None):
        """Initialize the Météo-France WS."""
        super().__init__(access_token)


class MeteoNetSession(MeteoFranceSession):
    """Session for MétéoNet."""

    host: str = METEONET_API_URL

    # TODO: convert to class method
    def __init__(self, access_token: Optional[str] = None):
        """Initialize the MétéoNet."""
        super().__init__(access_token)
