import logging
from swagger_server.services import kubernetes_adapter


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_edge_platform_nodes():
    '''
    Retrieves the nodes of the edge cloud platform supported by the testbed
    '''
    logger.info('Acquiring testbed nodes')
    try:
        nodes_list = kubernetes_adapter.get_nodes()
        return nodes_list
    except Exception as e:
        logger.info(e)
        return 'Error getting node list: '+e.args
