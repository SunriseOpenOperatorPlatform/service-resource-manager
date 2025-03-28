import connexion
import six

from swagger_server.models.apps_response import AppsResponse  # noqa: E501
from swagger_server.models.apps_response_apps import AppsResponseApps  # noqa: E501
from swagger_server.models.paas_registration_request import PaasRegistrationRequest  # noqa: E501
from swagger_server import util
from swagger_server.utils import connector_db
from swagger_server.utils import kubernetes_connector
from swagger_server.core import paas_handler
from swagger_server.utils import user_authentication

def deregister_paas(paas_service_name):  # noqa: E501
    """Deregister PaaS.

     # noqa: E501

    :param paas_service_name: Returns a  specific paas service from the catalogue.
    :type paas_service_name: str

    :rtype: None
    """

    role = user_authentication.check_role()
    if role is not None and role == "admin":
        try:
            status_deregistration = connector_db.delete_document_paas_service(paas_service_name)
            return status_deregistration
        except Exception as ce_:
            raise Exception("An exception occurred :", ce_)
    else:
        return "You are not authorized to access the URL requested", 401
def get_paas_services():  # noqa: E501
    """Returns PaaS Services from the catalogue.

     # noqa: E501

    :rtype: AppsResponse
    """
    try:
        paas_services = connector_db.get_documents_from_collection(collection_input="paas_services")
        return paas_services
    except Exception as ce_:
        raise Exception("An exception occurred :", ce_)


def get_paas_service(paas_service_name):  # noqa: E501
    """Returns a specific PaaS service from the catalogue.

     # noqa: E501

    :param paas_service_id: Returns a specific PaaS service from the catalogue.
    :type paas_service_id: str

    :rtype: AppsResponseApps
    """
    try:
        paas_service = connector_db.get_documents_from_collection("paas_services", input_type="_id",
                                                                      input_value=paas_service_name)
        if not paas_service:
            paas_service = connector_db.get_documents_from_collection("paas_services", input_type="name",
                                                                     input_value=paas_service_name)
            return paas_service
        else:
            return paas_service[0]
    except Exception as ce_:
        raise Exception("An exception occurred :", ce_)


def register_paas(body=None):  # noqa: E501
    """Register PaaS.

     # noqa: E501

    :param body: Registration method to save paas service into database
    :type body: dict | bytes

    :rtype: None
    """
    role = user_authentication.check_role()
    if role is not None and role == "admin":

        if connexion.request.is_json:
            body = PaasRegistrationRequest.from_dict(connexion.request.get_json())  # noqa: E501
            try:
                insert_doc=paas_handler.check_paas_registration(body)
                if not insert_doc:
                    return "Please provide the required input & check that referred service functions exist in the catalogue"
                else:
                    registration_status = connector_db.insert_document_paas(insert_doc)
                    return registration_status
            except Exception as ce_:
                return "An exception occurred: ", ce_
    else:
        return "You are not authorized to access the URL requested", 401


def update_paas(body=None):  # noqa: E501
    """Update PaaS registration.

     # noqa: E501

    :param body: Registration method to update paas service into database
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = PaasRegistrationRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
