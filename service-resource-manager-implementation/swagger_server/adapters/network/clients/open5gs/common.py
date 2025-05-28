# -*- coding: utf-8 -*-
# Common utilities (errors, HTTP helpers) used by the Open5GS client implementation (client.py).
from typing import Optional

from pydantic import BaseModel

from src import logger
from src.network.clients.errors import NetworkPlatformError

log = logger.get_logger(__name__)


class Open5GSError(NetworkPlatformError):
    pass


class Open5GSErrorResponse(BaseModel):
    message: str
    detail: dict


# --- HTTP Request Helper Functions ---
def open5gs_post(url: str, model_payload: BaseModel) -> dict:
    """
    Placeholder for the POST request function."""
    pass


def open5gs_get(url: str, params: Optional[dict] = None) -> dict:
    """
    Placeholder for the GET request function.
    """
    pass


def open5gs_delete(url: str) -> None:
    """
    Placeholder for the DELETE request function.
    """
    pass
