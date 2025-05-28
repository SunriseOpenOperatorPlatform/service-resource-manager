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
from __future__ import annotations

from typing import TYPE_CHECKING

from src.network.clients.oai.client import OaiNefClient
from src.network.clients.open5gcore.client import Open5GCoreClient
from src.network.clients.open5gs.client import Open5GSClient

if TYPE_CHECKING:
    from .network_interface import NetworkManagementInterface


class NetworkClientFactory:
    """
    Factory class for creating Network Management Clients.
    """

    @staticmethod
    def create_network_client(
        client_name: str, base_url: str
    ) -> NetworkManagementInterface:
        """
        Creates and returns an instance of the specified Network Client.
        """
        try:
            constructor = NetworkClientFactory.network_client_constructors[client_name]
            network_client_instance = constructor(base_url)
            return network_client_instance
        except KeyError:
            # Get the list of supported client names
            supported_clients = list(
                NetworkClientFactory.network_client_constructors.keys()
            )
            raise ValueError(
                f"Invalid network client name: '{client_name}'. "
                "Supported clients are: "
                f"{', '.join(supported_clients)}"
            )


class NetworkClientTypes:
    """
    Class for creating Network Clients.
    """

    OPEN5GS = "open5gs"
    OAI = "oai"
    OPEN5GCORE = "open5gcore"

    # --- Dictionary mapping type constants to constructors ---
    network_types = {
        OPEN5GS: lambda url: Open5GSClient(base_url=url),
        OAI: lambda url: OaiNefClient(base_url=url),
        OPEN5GCORE: lambda url: Open5GCoreClient(base_url=url),
    }
