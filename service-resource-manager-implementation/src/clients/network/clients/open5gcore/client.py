# -*- coding: utf-8 -*-
from src import logger
from src.network.core.network_interface import NetworkManagementInterface

log = logger.get_logger(__name__)


# TODO: Define any specific parameters or methods needed for Open5GCore
# In case any functionality is not implemented, raise NotImplementedError


class NetworkManager(NetworkManagementInterface):
    def __init__(self, base_url: str, scs_as_id: str):
        pass
