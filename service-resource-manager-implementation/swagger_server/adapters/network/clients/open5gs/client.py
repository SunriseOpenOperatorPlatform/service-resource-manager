# -*- coding: utf-8 -*-
from typing import Dict

from src import logger
from src.network.core.network_interface import NetworkManagementInterface

log = logger.get_logger(__name__)


class NetworkManager(NetworkManagementInterface):
    """
    This client implements the NetworkManagementInterface and translates the
    CAMARA APIs into specific HTTP requests understandable by the Open5GS NEF API.

    Invloved partners and their roles in this implementation:
    - I2CAT: Responsible for the CAMARA QoD API and its mapping to the
             3GPP AsSessionWithQoS API exposed by Open5GS NEF.
    - NCSRD: Responsible for the CAMARA Location API and its mapping to the
             3GPP Monitoring Event API exposed Open5GS NEF.
    """

    def __init__(self, base_url: str, scs_as_id: str):
        """
        Initializes the Open5GS Client.
        """
        try:
            self.base_url = base_url
            self.scs_as_id = scs_as_id
            log.info(
                f"Initialized Open5GSClient with base_url: {self.base_url} "
                f"and scs_as_id: {self.scs_as_id}"
            )
        except Exception as e:
            log.error(f"Failed to initialize Open5GSClient: {e}")
            raise e

    # --- Implementation of NetworkManagementInterface methods ---
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoD session based on the CAMARA QoD API input.
        Maps the CAMARA QoD POST /sessions to Open5GS NEF POST /{scsAsId}/subscriptions.
        """
        pass

    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves a specific Open5GS QoS Subscription details.
        Maps CAMARA QoD GET /sessions/{sessionId} to Open5GS NEF GET /
        {scsAsId}/subscriptions/{subscriptionId}.
        """
        pass

    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Open5GS QoS Subscription.
        Maps CAMARA QoD DELETE /sessions/{sessionId} to Open5GS NEF DELETE /
        {scsAsId}/subscriptions/{subscriptionId}.
        """
        pass


# Note:
# As this class is inheriting from NetworkManagementInterface, it is
# expected to implement all the abstract methods defined in that interface.
#
# In case this network adapter doesn't support a specific method, it should
# be marked as NotImplementedError.
