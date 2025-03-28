import connexion
import six
from swagger_server.models.apps_response import AppsResponse  # noqa: E501
from swagger_server.models.apps_response_apps import AppsResponseApps  # noqa: E501
from swagger_server.models.service_function_registration_request import ServiceFunctionRegistrationRequest  # noqa: E501
from swagger_server import util
from swagger_server.utils import connector_db
from swagger_server.utils import kubernetes_connector, user_authentication
import logging
import os

logger=logging.getLogger(__name__)

adapter_name = os.environ['EDGE_CLOUD_ADAPTER_NAME']
edge_cloud_provider = os.environ['PLATFORM_PROVIDER']
adapter = None

if adapter_name=='aeros':
     from adapters.edgecloud.clients.aeros.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='i2edge':
     from adapters.edgecloud.clients.i2edge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='eurecom_platform':
     from adapters.edgecloud.clients.eurecom_platform.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='piedge':
     from adapters.edgecloud.clients.piedge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()

def deregister_service_function(id: str):  # noqa: E501
    """Deregister service.

     # noqa: E501

    :param service_function_name: Returns a  specific service function from the catalogue.
    :type service_function_name: str

    :rtype: None


    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":
        try:

            # status_deregistration=connector_db.delete_document_service_function(service_function_name)
            status_deregistration = adapter.delete_onboarded_app(id)
            return status_deregistration
        except Exception as ce_:
            raise Exception("An exception occurred :", ce_)

    else:
        return "You are not authorized to access the URL requested", 401


def get_service_function(id: str):  # noqa: E501
    """Returns a specific service function from the catalogue.

     # noqa: E501

    :param service_function_id: Returns a  specific service function from the catalogue.
    :type service_function_id: str

    :rtype: AppsResponseApps
    """

    try:
        # service_function = connector_db.get_documents_from_collection("service_functions", input_type="name",
        #                                                                   input_value=service_function_name)
        service_function = adapter.get_onboarded_app(id)
        return service_function
        # else:
        #     return service_function[0]
    except Exception as ce_:
        raise Exception("An exception occurred :", ce_)


def get_service_functions():  # noqa: E501
    """Returns service functions from the catalogue.

     # noqa: E501


    :rtype: AppsResponse
    """
    try:
        # service_functions = connector_db.get_documents_from_collection(collection_input="service_functions")
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

    role = user_authentication.check_role()
    if role is not None and role == "admin":
        if connexion.request.is_json:
            body = adapter.onboard_app(connexion.request.get_json())
            # body = ServiceFunctionRegistrationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            insert_doc = body.to_dict()
            try:
                result=connector_db.insert_document_service_function(insert_doc)
                if result.acknowledged is True:
                    return {'appId': str(result.inserted_id)}
                else:
                    return 'Error inserting new application', 400
            except Exception as ce_:
                return ce_
    else:
        return "You are not authorized to access the URL requested", 401

#TODO!!!!
def update_service_function(body=None):  # noqa: E501
    """Update Service registration.

     # noqa: E501

    :param body: Registration method to update service function into database
    :type body: dict | bytes

    :rtype: None
    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":
        if connexion.request.is_json:
            body = ServiceFunctionRegistrationRequest.from_dict(connexion.request.get_json())  # noqa: E501

            insert_doc = body.to_dict()
            # insert_doc["kubernetesPlatformName"] = body.kubernetes_platform_name
            # insert_doc["kubernetesAuthCredentials"] = body.kubernetes_auth_credentials.to_dict()
            try:
                response_status = connector_db.update_document_service_function(insert_doc)
                return response_status
            except Exception as ce_:
                raise Exception("An exception occurred :", ce_)
    else:
        return "You are not authorized to access the URL requested", 401
