# -*- coding: utf-8 -*-
from typing import Dict

from src import logger
from src.network.core.network_interface import NetworkManagementInterface

log = logger.get_logger(__name__)


# Placeholder for the Open5gcore Network Management Client
class NetworkManager(NetworkManagementInterface):
    def __init__(self, base_url: str, scs_as_id: str):
        pass

    def create_qod_session(self, session_info: Dict) -> Dict:
        pass

    def get_qod_session(self, session_id: str) -> Dict:
        pass

    def delete_qod_session(self, session_id: str) -> None:
        pass


# Note:
# As this class is inheriting from NetworkManagementInterface, it is
# expected to implement all the abstract methods defined in that interface.
#
# In case this network adapter doesn't support a specific method, it should
# be marked as NotImplementedError.
