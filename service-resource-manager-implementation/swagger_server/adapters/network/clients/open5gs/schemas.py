# -*- coding: utf-8 -*-
# This file defines the Pydantic models that represent the data structures (schemas)
# for the requests sent to and responses received from the Open5GS NEF API,
# specifically focusing on the APIs needed to support CAMARA QoD.

from pydantic import BaseModel


# Dummy examples of Pydantic models for the Open5GS NEF API.
class Open5GSQoSSubscription(BaseModel):
    """
    Represents the payload for creating a QoS subscription in Open5GS.
    """

    pass


class CamaraQoDSessionInfo(BaseModel):
    """
    Represents the input data for creating a QoD session.
    """

    pass
