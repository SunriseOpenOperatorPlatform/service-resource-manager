from os import environ
import logging
import connexion

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


network_client = environ.get('NETWORK_CLIENT')
adapter = None

if network_client is not None:
    if network_client=='oai':
        from src.clients.network.clients.oai.client import NetworkManager
        adapter = NetworkManager()
    elif network_client=='open5gcore':
        from src.clients.network.clients.open5gcore.client import NetworkManager
        adapter = NetworkManager()
    else:
        from src.clients.network.clients.open5gs.client import NetworkManager
        adapter = NetworkManager()


def create_qod_session(body):
    if connexion.request.is_json:
        try:
            response = adapter.create_qod_session(body)
            return response
        except Exception as ce_:
            logger.error(ce_)
        return ce_
    else:
        return 'ERROR: Could not read JSON payload.', 400

def get_qod_session(id: str):
    try:
        response = adapter.get_qod_session(id)
        return response
    except Exception as ce_:
            logger.error(ce_)
    return ce_

def delete_qod_session(id: str):
    try:
        response = adapter.delete_qod_session(id)
        return 'QoD successfully removed'
    except Exception as ce_:
            logger.error(ce_)
    return ce_

def create_traffic_influence_resource(body):
     pass

def delete_traffic_influence_resource(id: str):
     pass

def get_traffic_influence_resource(id: str):
     pass

def get_all_traffic_influence_resources():
     pass