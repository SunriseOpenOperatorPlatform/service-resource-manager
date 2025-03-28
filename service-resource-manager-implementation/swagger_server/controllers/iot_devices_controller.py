import connexion
import six

from swagger_server.models.add_iot_device import AddIotDevice  # noqa: E501
from swagger_server import util

from swagger_server.utils import iot_devices
from swagger_server.utils import user_authentication

def add_iot_device(body=None):  # noqa: E501
    """Adds an IoT Device

     # noqa: E501

    :param body: Adds an IoT Device
    :type body: dict | bytes

    :rtype: None
    """

    role = user_authentication.check_role()

    if role is not None and role == "admin":
            if connexion.request.is_json:
                try:
                    body = AddIotDevice.from_dict(connexion.request.get_json())  # noqa: E501
                    response=iot_devices.create_value_and_device(body)
                    return response
                except Exception as ce_:
                    raise Exception("An exception occurred :", ce_)

    else:
        return "You are not authorized to access the URL requested", 401
