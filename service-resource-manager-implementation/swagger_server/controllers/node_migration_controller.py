import connexion
import six

from swagger_server.models.service_function_node_migration import ServiceFunctionNodeMigration  # noqa: E501
from swagger_server import util
from swagger_server.utils import user_authentication, kubernetes_connector, connector_db


def service_function_node_migration(body=None):  # noqa: E501
    """Migrates service function from one node to another

     # noqa: E501

    :param body: Migrates service function from one node to another
    :type body: dict | bytes

    :rtype: None
    """

    role = user_authentication.check_role()
    if role is not None and role == "admin":

        if connexion.request.is_json:
            body = ServiceFunctionNodeMigration.from_dict(connexion.request.get_json())  # noqa: E501



            if body.destination_location is not None:
                loc = connector_db.get_documents_from_collection("points_of_presence", input_type="location",
                                                                   input_value=body.destination_location)
                if not loc:
                    return "The given location does not exist in the node catalogue"

            deploy = kubernetes_connector.operate_service_function_node_migration(body)

            return deploy

    else:
        return "You are not authorized to access the URL requested", 401


