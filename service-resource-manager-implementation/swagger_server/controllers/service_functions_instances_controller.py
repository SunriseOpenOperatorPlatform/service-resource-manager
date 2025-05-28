import connexion
import six

from swagger_server.models.deploy_chain import DeployChain  # noqa: E501
from swagger_server.models.deploy_service_function import DeployServiceFunction  # noqa: E501
from swagger_server.models.deployedapps_response import DeployedappsResponse  # noqa: E501
from swagger_server.models.edge_cloud_zone import EdgeCloudZone
from swagger_server.models.deploy_app import DeployApp
from swagger_server import util
from swagger_server.core import piedge_encoder
from swagger_server.utils import connector_db, nodes_monitoring
from swagger_server.utils import kubernetes_connector,auxiliary_functions, user_authentication
import os
import logging


logger=logging.getLogger(__name__)
# driver=os.environ['DRIVER'].strip()

adapter_name = os.environ['EDGE_CLOUD_ADAPTER_NAME']
edge_cloud_provider = os.environ['PLATFORM_PROVIDER']
adapter = None

if adapter_name=='aeros':
     from swagger_server.adapters.edgecloud.clients.aeros.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='i2edge':
     from swagger_server.adapters.edgecloud.clients.i2edge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='eurecom_platform':
     from swagger_server.adapters.edgecloud.clients.eurecom_platform.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='piedge':
     from swagger_server.adapters.edgecloud.clients.piedge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()

def delete_chain(chain_service_name):  # noqa: E501
    """Deletes a deployed chain.

     # noqa: E501

    :param chain_service_name: Represents a chain Service  from the running deployments.
    :type chain_service_name: str

    :rtype: None
    """
    return 'do some magic!'


def delete_deployed_service_function(app_id: str):  # noqa: E501
    """Deletes a deployed Service function.

     # noqa: E501

    :param deployed_service_function_name: Represents a service function from the running deployments.
    :type deployed_service_function_name: str

    :rtype: None
    """

    # role = user_authentication.check_role()
    # if role is not None and role == "admin":
    response = None
    try:
                response = adapter.undeploy_app(app_id)
                # deployed_service_function_name_=auxiliary_functions.prepare_name_for_k8s(deployed_service_function_name)
                # sfs=kubernetes_connector.get_deployed_service_functions()

                # for service_fun in sfs:
                #     if service_fun["service_function_instance_name"]==deployed_service_function_name:
                #         kubernetes_connector.delete_service_function(deployed_service_function_name_)

                #         # if "monitoring_service_URL" in service_fun:
                #         #     nodes_monitoring.delete_monitoring_for_service_function(deployed_service_function_name)

                #         return "Service function deployment deleted"

                return response

    except Exception as ce_:
        logger.error(ce_)
        return ce_
    # else:
    #     return "You are not authorized to access the URL requested", 401


def deploy_chain(body=None):  # noqa: E501
    """Request to deploy a chain of function services.

     # noqa: E501

    :param body: Deploy chain.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = DeployChain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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
    # else:
    #     return "You are not authorized to access the URL requested", 401


def deployed_service_function_status(deployed_service_function_name):  # noqa: E501
    """Returns the requested edge service status per node.

     # noqa: E501

    :param deployed_service_function_name: Represents a  service function  from the running deployments
    :type deployed_service_function_name: str

    :rtype: DeployedappsResponse
    """
    try:
        final_response = {}
        response = kubernetes_connector.get_deployed_service_functions()
        if response:
            for sf in response:
                if sf["service_function_instance_name"] == deployed_service_function_name:
                    final_response = sf
                    break

                if sf["service_function_instance_name"] == deployed_service_function_name.lower():
                    final_response = sf
                    break
        return final_response
    except Exception as ce_:
        logging.info(ce_)
        return ce_.args


def deployed_service_functions_status():  # noqa: E501
    """Returns the edge service functions status per node.

     # noqa: E501

    :rtype: DeployedappsResponse
    """
    # role = user_authentication.check_role()
    # if role is not None and role == "admin":
    try:
            # response = kubernetes_connector.get_deployed_service_functions()
        response = adapter.get_all_deployed_apps()
        return response
    except Exception as ce_:
        logger.error(ce_)
        return ce_
    # else:
    #     return "You are not authorized to access the URL requested", 401    


def update_chain(body=None):  # noqa: E501
    """Request to update a chain of function services.

     # noqa: E501

    :param body: Deploy chain.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = DeployChain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_deployed_service_function(body=None):  # noqa: E501
    """Request to update the status of a service.

     # noqa: E501

    :param body: update a running service function.
    :type body: dict | bytes

    :rtype: None
    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":
        if connexion.request.is_json:
            try:
                body = DeployServiceFunction.from_dict(connexion.request.get_json())  # noqa: E501
                
            except Exception as ce_:
                logger.error(ce_)
                return ce_
        else:
            return 'ERROR: Could not read JSON payload.'
    else:
        return "You are not authorized to access the URL requested", 401
