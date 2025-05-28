# Mocked API for testing purposes
from typing import Dict, List, Optional
import os
import logging
import requests
from swagger_server.adapters.edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface
from swagger_server.utils import kubernetes_connector, connector_db
from swagger_server.models.service_function_registration_request import ServiceFunctionRegistrationRequest
from swagger_server.models.deploy_service_function import DeployServiceFunction
from swagger_server.models.app_manifest import AppManifest
from swagger_server.core.piedge_encoder import deploy_service_function

# piedge_ip = os.environ['EDGE_CLOUD_ADAPTER_IP']
edge_cloud_provider = os.environ['PLATFORM_PROVIDER']

class EdgeApplicationManager(EdgeCloudManagementInterface):
    def onboard_app(self, app_manifest: AppManifest) -> Dict:
        print(f"Submitting application: {app_manifest}")
        logging.info('Extracting variables from payload...')
        app_name = app_manifest.get('name')
        image = app_manifest.get('appRepo').get('imagePath')
        package_type = app_manifest.get('packageType')
        network_interfaces = app_manifest.get('componentSpec')[0].get('networkInterfaces')
        ports = []
        for ni in network_interfaces:
            ports.append(ni.get('port'))
        insert_doc = ServiceFunctionRegistrationRequest(service_function_image=image, service_function_name=app_name, service_function_type=package_type, application_ports=ports)
        result = connector_db.insert_document_service_function(insert_doc.to_dict())
        return {'appId': str(result.inserted_id)}

    def get_all_onboarded_apps(self) -> List[Dict]:
        logging.info('Retrieving all registered apps from database...')
        db_list = connector_db.get_documents_from_collection(collection_input="service_functions")
        app_list = []
        for sf in db_list:
            app_list.append(self.__transform_to_camara(sf))
        return app_list
        # return [{"appId": "1234-5678", "name": "TestApp"}]

    def get_onboarded_app(self, app_id: str) -> Dict:
        logging.info('Searching for registered app with ID: '+ app_id+' in database...')
        app = connector_db.get_documents_from_collection("service_functions", input_type="_id", input_value=app_id)
        if len(app)>0:
            return self.__transform_to_camara(app[0])
        else:
            return []

    def delete_onboarded_app(self, app_id: str) -> None:
        logging.info('Deleting registered app with ID: '+ app_id+' from database...')
        result, code = connector_db.delete_document_service_function(_id=app_id)
        print(f"Removing application metadata: {app_id}")
        return result, code

    def deploy_app(self, app_id: str, app_zones: List[Dict]) -> Dict:
        logging.info('Searching for registered app with ID: '+ app_id+' in database...')
        app = connector_db.get_documents_from_collection("service_functions", input_type="_id", input_value=app_id)
        success_response = []
        if len(app)<1:
            return 'Application with ID: '+ app_id+' not found', 404
        if app is not None:
            logging.info(app_zones)
            for zone in app_zones:
                sf = DeployServiceFunction(service_function_name=app[0].get('name'), 
                                           service_function_instance_name=app[0].get('name')+'-'+zone.get('EdgeCloudZone').get('edgeCloudZoneName'), 
                                           location=zone.get('edgeCloudZoneName'))
                result = deploy_service_function(service_function=sf)
                success_response.append(result)
        # return {"appInstanceId": "abcd-efgh"}
        return success_response

    def get_all_deployed_apps(self, app_id: Optional[str] = None, app_instance_id: Optional[str] = None, region: Optional[str] = None) -> List[Dict]:
        logging.info('Retreiving all deployed apps in the edge cloud platform')
        deployments = kubernetes_connector.get_deployed_service_functions()
        response = []
        for deployment in deployments:
            item = {}
            item['appInstanceId'] = deployment.get('uid')
            item['status'] = deployment.get('status')
            item['componentEndpointInfo'] = {}
            item['kubernetesClusterRef'] = ""
            item['edgeCloudZone'] = {}
            response.append(item)
        return response
        # return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    def undeploy_app(self, app_instance_id: str) -> None:
        logging.info('Searching for deployed app with ID: '+ app_instance_id+' in database...')
        print(f"Deleting app instance: {app_instance_id}")
        # deployed_service_function_name_=auxiliary_functions.prepare_name_for_k8s(deployed_service_function_name)
        sfs=kubernetes_connector.get_deployed_service_functions()
        response = 'App instance with ID ['+app_instance_id+'] not found'
        for service_fun in sfs:
            if service_fun["uid"]==app_instance_id:
                kubernetes_connector.delete_service_function(service_fun['service_function_instance_name'])
                response = 'App instance with ID ['+app_instance_id+'] successfully removed'
                break
        return response


    def get_edge_cloud_zones(self, region: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        
        nodes_response = kubernetes_connector.get_PoPs()
        zone_list =[]
        
        for node in nodes_response:
                zone = {}
                zone['edgeCloudZoneId'] = node.get('uid')
                zone['edgeCloudZoneName'] = node.get('name')
                zone['edgeCloudZoneStatus'] = node.get('status')
                zone['edgeCloudProvider'] = edge_cloud_provider
                zone['edgeCloudRegion'] = node.get('location')
                zone_list.append(zone)
        return zone_list
    
    def __transform_to_camara(self, app_data):
        app = {}
        app['appId'] = app_data.get('_id')
        app['name'] = app_data.get('name')
        app['packageType'] = app_data.get('type')
        appRepo = {'imagePath': app_data.get('image')}
        app['appRepo'] = appRepo
        networkInterfaces = []
        for port in app_data.get('application_ports'):
            port_spec = {'protocol': 'TCP', 'port': port}
            networkInterfaces.append(port_spec)
        app['componentSpec'] = [{'componentName': app_data.get('name'), 'networkInterfaces': networkInterfaces}]
        return app
