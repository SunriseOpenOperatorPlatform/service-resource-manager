from __future__ import absolute_import
import logging
from os import environ
import requests
import json
from src.clients.edgecloud.clients import aeros, i2edge, piedge


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

adapter_name = environ['ADAPTER_NAME']
adapter_ip = environ['K8S_ADAPTER_ADDRESS']
edge_cloud_provider = environ['PLATFORM_PROVIDER']
adapter = None

if adapter_name=='aeros':
     from src.clients.edgecloud.clients.aeros.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='i2edge':
     from src.clients.edgecloud.clients.i2edge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()
elif adapter_name=='piedge':
     from src.clients.edgecloud.clients.piedge.client import EdgeApplicationManager
     adapter = EdgeApplicationManager()


def get_nodes():
    zone_list = None
    return zone_list

def submit_helm_chart(body):
     logger.info('Contacting Kubernetes adapter at '+adapter_ip)
     headers = {'Content-type': 'application/json'}
     data = json.dumps(body)
     helm_response = requests.post('http://'+adapter_ip+'/piedge-connector/2.0.0/helm', data=data, headers=headers)
     return helm_response

# def app_instance_deploy(body):
#      logger.info('Contacting Kubernetes adapter at '+adapter_ip)
#      headers = {'Content-type': 'application/json'}
#      data = json.dumps(body)
#      app_response = requests.post('http://'+adapter_ip+'/piedge-connector/2.0.0/deployedServiceFunction', json=body)
#      return app_response

def app_instance_info(id: str):
     logger.info('Contacting Kubernetes adapter at '+adapter_ip)
     headers = {'Content-type': 'application/json'}
     app_info_response = requests.get('http://'+adapter_ip+'/piedge-connector/2.0.0/deployedServiceFunction/'+id)
     return app_info_response

def delete_app_instance(id: str):
     logger.info('Deleting app with instance id: ['+id+']')
     delete_app_response = requests.delete('http://'+adapter_ip+'/piedge-connector/2.0.0/deployedServiceFunction/'+id)
     return delete_app_response