#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Reza Mosahebfard (reza.mosahebfard@i2cat.net)
##
from abc import ABC, abstractmethod
from typing import Dict


class NetworkManagementInterface(ABC):
    """
    Abstract Base Class for Network Resource Management.

    This interface defines the standard methods that all
    Network Clients (Open5GS, OAI, Open5GCore) must implement.

    Partners implementing a new network client should inherit from this class
    and provide concrete implementations for all abstract methods relevant
    to their specific NEF capabilities.
    """

    @abstractmethod
    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoS session based on CAMARA QoD API input.

        args:
            session_info: Dictionary containing session details conforming to
                          the CAMARA QoD session creation parameters.

        returns:
            dictionary containing the created session details, including its ID.
        """
        pass

    @abstractmethod
    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves details of a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session.

        returns:
            Dictionary containing the details of the requested QoS session.
        """
        pass

    @abstractmethod
    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session to delete.

        returns:
            None
        """
        pass

    # Placeholder for other CAMARA APIs (e.g., Traffic Influence,
    # Location-retrieval, etc.)
