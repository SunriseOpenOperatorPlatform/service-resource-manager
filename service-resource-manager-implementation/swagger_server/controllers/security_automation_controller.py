import connexion
import six
import requests
# import logging
from swagger_server.models.activate_secured_slice import ActivateSecuredSlice  # noqa: E501
from swagger_server import util


def activate_secured_slice(body=None):  # noqa: E501
    """Enables a secured slice

     # noqa: E501

    :param body: Creates a secured slice
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ActivateSecuredSlice.from_dict(connexion.request.get_json())  # noqa: E501
        insert_doc = body.to_dict()
        url = 'http://203.0.113.9:3090/security/1.0.0/activateSecurity'
        myobj = {'hostname': body.slice_name}
        x = requests.post(url, json=myobj)

    return x.status_code


def delete_secured_slice(slice_name):  # noqa: E501
    """Disables security monitoring over a slice


     # noqa: E501

    :param slice_name: Represents a slice from the running slices.
    :type slice_name: str

    :rtype: None
    """
    return 'do some magic!'
