from __future__ import print_function
import os
import time
from swagger_server.utils import connector_db
import requests
from requests.structures import CaseInsensitiveDict
# import traceback
# import logging


mec_ip=os.environ["MEC_PLATFORM_IP"].strip()
mec_port=os.environ["MEC_PLATFORM_PORT"].strip()
host = "http://" + mec_ip + ":" + mec_port

def get_services(serviceid):

    if serviceid is None:
        url = host + "/mec_platform/applications/mec_dataspace_connectors/services"
    else:
        url=host + "/mec_platform/applications/mec_dataspace_connectors/services/"+serviceid

    response = requests.post(url, verify=False)
    return response


def deregister_service(service_id):
    url = host + "/mec_platform/applications/mec_dataspace_connectors/services/"+service_id
    response = requests.delete(url, verify=False)
    return response



def register_service(service_url, service_name, service_id):

    json_body= {
                              "serInstanceId": service_id,
                              "serName": service_name,
                              "serCategory": {
                                "href": "string",
                                "id": "1",
                                "name": "dataspace_connector",
                                "version": "string"
                              },
                              "version": "1.0",
                              "state": "ACTIVE",
                              "transportInfo": {
                                "id": "string",
                                "name": "string",
                                "description": "string",
                                "type": "REST_HTTP",
                                "protocol": "string",
                                "version": "string",
                                "security": {
                                  "oAuth2Info": {
                                    "grantTypes": [
                                      "OAUTH2_AUTHORIZATION_CODE"
                                    ],
                                    "tokenEndpoint": "string"
                                  }
                                },
                                "implSpecificInfo": {}
                              },
                              "serializer": "JSON",
                              "scopeOfLocality": "MEC_SYSTEM",
                              "consumedLocalOnly": True,
                              "isLocal": True,
                              "livenessInterval": 0,
                              "_links": {
                                "self": {
                                  "href": service_url
                                },
                                "liveness": {
                                  "href": "string"
                                }
                              }
                            }
    try:
        url = host + "/mec_platform/applications/mec_dataspace_connectors/services"
        #headers = {"Authorization": "Bearer " + token_k8s}
        response = requests.post(url, json=json_body, verify=False)
        return response
    except requests.exceptions.HTTPError as e:
        return ("Exception when calling  POST at mec_platform/applications/mec_dataspace_connectors/services\n" % e)