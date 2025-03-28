import connexion
import six
import logging
import os

from swagger_server.models.deploy_chain import DeployChain  # noqa: E501
from swagger_server.models.deploy_paas import DeployPaas  # noqa: E501
from swagger_server.models.deployedapps_response import DeployedappsResponse  # noqa: E501
from swagger_server import util
from swagger_server.core import paas_handler
from swagger_server.core import ids_connector_handler
from swagger_server.utils import user_authentication



from flask import Flask, Response, json

logger=logging.getLogger(__name__)

driver=os.environ['DRIVER'].strip()


def delete_deployed_paas_service(deployed_paas_service_name):  # noqa: E501
    """Deletes a deployed PaaS service.

     # noqa: E501

    :param deployed_paas_service_name: Represents a paas  from the running deployments.
    :type deployed_paas_service_name: str

    :rtype: None
    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":
        try:
            response=paas_handler.operate_paas_delete_deployment_request(deployed_paas_service_name)
            return response
        except Exception as ce_:
            return ("An exception occurred :", ce_)

    else:
        return "You are not authorized to access the URL requested", 401


def deploy_paas(body=None):  # noqa: E501
    """Request to deploy a PaaS (from the catalogue) to an edge node.

     # noqa: E501

    :param body: Deploy PaaS.
    :type body: dict | bytes

    :rtype: None
    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":
        if connexion.request.is_json:
            body = DeployPaas.from_dict(connexion.request.get_json())  # noqa: E501
            try:
                response = paas_handler.operate_paas_deployment_request(body)
                return  response

            # if body.data_space_enabled is not None:
            #     if body.data_space_enabled:
            #         ids_connector_handler.deploy_ids_connector(body.paas_instance_name)

            except Exception as ce_:
                logger.error(ce_)
                return ce_
    else:
        return "You are not authorized to access the URL requested", 401



def deployed_paas_service_status(deployed_paas_service_name):  # noqa: E501
    """Returns the requested edge paas service status.

     # noqa: E501

    :param deployed_paas_service_name: Represents a paas  from the running deployments.
    :type deployed_paas_service_name: str

    :rtype: DeployedappsResponse
    """

    try:
        response = paas_handler.get_deployed_paas_services(deployed_paas_service_name)
        # response = kubernetes_connector.get_deployed_service_functions()
        return response
    except Exception as ce_:
        logger.error(ce_)
        return ce_.args


def deployed_paas_services_status():  # noqa: E501
    """Returns edge paas services status.

     # noqa: E501


    :rtype: DeployedappsResponse
    """

    try:
        response = paas_handler.get_deployed_paas_services()
        #response = kubernetes_connector.get_deployed_service_functions()
        return response
    except Exception as ce_:
        logger.error(ce_)
        return ce_


def update_deployed_paas(body=None):  # noqa: E501
    """Request to update the status of a deployed PaaS.

     # noqa: E501

    :param body: update a running paas.
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = DeployChain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
