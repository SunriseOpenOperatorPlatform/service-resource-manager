import connexion
import six
import logging
import os

logger=logging.getLogger(__name__)

adapter_name = os.environ['EDGE_CLOUD_ADAPTER_NAME']
adapter_base_url = os.environ['ADAPTER_BASE_URL']
adapter = None

if adapter_name=='aeros':
     from src.clients.edgecloud.clients.aeros.client import EdgeApplicationManager
     adapter = EdgeApplicationManager(base_url=adapter_base_url)
elif adapter_name=='i2edge':
     from src.clients.edgecloud.clients.i2edge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager(base_url=adapter_base_url)
elif adapter_name=='kubernetes':
     from src.clients.edgecloud.clients.piedge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager(base_url=adapter_base_url, **os.environ)

def deregister_service_function(service_function_id: str):  # noqa: E501
    """Deregister service.

     # noqa: E501

    :param service_function_name: Returns a  specific service function from the catalogue.
    :type service_function_name: str

    :rtype: None


    """
    try:
            status_deregistration, code = adapter.delete_onboarded_app(service_function_id)
            return status_deregistration, code
    except Exception as ce_:
            raise Exception("An exception occurred :", ce_)


def get_service_function(service_function_id: str):  # noqa: E501
    """Returns a specific service function from the catalogue.

     # noqa: E501

    :param service_function_id: Returns a  specific service function from the catalogue.
    :type service_function_id: str

    :rtype: AppsResponseApps
    """

    try:
        service_function = adapter.get_onboarded_app(service_function_id)
        return service_function
    except Exception as ce_:
        raise Exception("An exception occurred :", ce_)


def get_service_functions():  # noqa: E501
    """Returns service functions from the catalogue.

     # noqa: E501


    :rtype: AppsResponse
    """
    try:
        service_functions = adapter.get_all_onboarded_apps()
        return service_functions
    except Exception as ce_:
        raise Exception("An exception occurred :", ce_)


def register_service_function(body=None):  # noqa: E501
    """Register Service.

     # noqa: E501

    :param body: Registration method to save service function into database
    :type body: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:

            insert_doc = connexion.request.get_json()
            try:
                 return adapter.onboard_app(insert_doc)
            except Exception as ce_:
                return ce_

def delete_deployed_service_function(app_id: str):  # noqa: E501
    """Deletes a deployed Service function.

     # noqa: E501

    :param deployed_service_function_name: Represents a service function from the running deployments.
    :type deployed_service_function_name: str

    :rtype: None
    """

    response = None
    try:
                response = adapter.undeploy_app(app_id)
                # return response

    except Exception as ce_:
        logger.error(ce_)
        return ce_
    # else:
    #     return "You are not authorized to access the URL requested", 401


def deploy_service_function():  # noqa: E501
    """Request to deploy a Service function (from the catalogue) to an edge node.

     # noqa: E501

    :param body: Deploy Service Function.
    :type body: dict | bytes

    :rtype: None
    """

    # role = user_authentication.check_role()
    # if role is not None and role == "admin":
    if connexion.request.is_json:
            try:
                # body = DeployApp.from_dict(connexion.request.get_json())
                body = connexion.request.get_json()
                response = adapter.deploy_app(app_id=body.get("appId"), app_zones=body.get("appZones"))
                # body = DeployServiceFunction.from_dict(connexion.request.get_json())
                # response = piedge_encoder.deploy_service_function(body)
                return response
            except Exception as ce_:
                logger.error(ce_)
                return ce_
    else:
            return 'ERROR: Could not read JSON payload.'
    
def get_deployed_service_functions():  # noqa: E501
    """Request to deploy a Service function (from the catalogue) to an edge node.

     # noqa: E501

    :param body: Deploy Service Function.
    :type body: dict | bytes

    :rtype: None
    """

    # role = user_authentication.check_role()
    # if role is not None and role == "admin":
    try:
            response = adapter.get_all_deployed_apps()
            return response
    except Exception as ce_:
                logger.error(ce_)
                return ce_

def get_deployed_service_function(app_id: str):  # noqa: E501
    """Request to deploy a Service function (from the catalogue) to an edge node.

     # noqa: E501

    :param body: Deploy Service Function.
    :type body: dict | bytes

    :rtype: None
    """

    # role = user_authentication.check_role()
    # if role is not None and role == "admin":
    try:
            response = adapter.get_deployed_app(app_id=app_id)
            return response
    except Exception as ce_:
                logger.error(ce_)
                return ce_

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