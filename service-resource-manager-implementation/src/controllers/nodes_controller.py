import connexion
import six
import time
from src.core import piedge_encoder
import logging
# from src.__main__ import driver
import os


logger=logging.getLogger(__name__)

adapter_name = os.environ['EDGE_CLOUD_ADAPTER_NAME']
adapter = None

if adapter_name=='aeros':
     from src.clients.edgecloud.clients.aeros.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='i2edge':
     from src.clients.edgecloud.clients.i2edge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='piedge':
     from src.clients.edgecloud.clients.piedge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()


def get_nodes():  # noqa: E501
    """Returns the edge nodes status.

     # noqa: E501

    :rtype: NodesResponse
    """
    try:
         response = adapter.get_edge_cloud_zones()
         return response
    except Exception as ce_:
            logger.info(ce_)
