from os import environ
import logging
from swagger_server.adapters.kubernetes_adapter import submit_helm_chart, app_deploy
import connexion

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def deploy_app(helm_request_body=None):
    '''
    Retrieves the nodes of the edge cloud platform supported by the testbed
    '''
    logger.info('Submitting request to edge cloud transformation function')
    if connexion.request.is_json:
        helm_request_body = connexion.request.get_json()
    else:
        return 'Wrong request schema', 400
    try:
        if helm_request_body.get('uri') is None:
            return 'Helm chart uri is missing', 400
        if helm_request_body.get('deployment_name') is None:
            return 'Helm chart deployment name is missing', 400
        
        helm_submit_response = submit_helm_chart(helm_request_body)
        return helm_submit_response
    except Exception as e:
        logger.info(e)
        return 'Error submitting helm chart: '+e.__cause__
    
def get_app_instances(body):
    '''
    Instantiates app on the edge cloud platform
    '''
    logger.info('Deploying app instance')
    if connexion.request.is_json:
        helm_request_body = connexion.request.get_json()
    else:
        return 'Wrong request schema', 400
    try:
        app_response = app_deploy(body)
    except Exception as e:
        logger.info(e)
        return 'Error instantiating app: '+e.__cause__
    