# -*- coding: utf-8 -*-
"""Session managers for the Météo-France REST API."""
from typing import Any
from typing import Optional

from requests import Response
from requests import Session

from .const import METEOFRANCE_API_TOKEN
from .const import METEOFRANCE_API_URL


class MeteoFranceSession(Session):
    """HTTP session manager for Météo-France.

    This session object allows to manage the authentication in the API using a token.
    """

    host: str = METEOFRANCE_API_URL

    def __init__(self, access_token: Optional[str] = None) -> None:
        """Initialize the authentication.

        Args:
            access_token: a string containing the authentication token for the REST API.
        """
        self.access_token = access_token or METEOFRANCE_API_TOKEN
        Session.__init__(self)

    def request(  # type: ignore
        self, method: str, path: str, *args: Any, **kwargs: Any
    ) -> Response:
        """Make a request using token authentication.

        Args:
            method: Method for the HTTP request (example "get").
            path: path of the REST API endpoint.
            args: all other non-keyword arguments.
            kwargs: all other keyword arguments.

        Returns:
            the Response object corresponding to the result of the API request.
        """
        params_inputs = kwargs.pop("params", None)

        params = {"token": self.access_token}
        if params_inputs:
            params.update(params_inputs)

        kwargs["params"] = params
        response = super().request(method, f"{self.host}/{path}", *args, **kwargs)
        response.raise_for_status()

        return response
