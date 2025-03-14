# Mocked API for testing purposes
from typing import Dict, List, Optional
import os
import logging
import requests
from edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface

piedge_ip = os.environ['EDGE_CLOUD_ADAPTER']
edge_cloud_provider = os.environ['PLATFORM_PROVIDER']

class EdgeApplicationManager(EdgeCloudManagementInterface):
    def onboard_app(self, app_manifest: Dict) -> Dict:
        print(f"Submitting application: {app_manifest}")
        return {"appId": "1234-5678"}

    def get_all_onboarded_apps(self) -> List[Dict]:
        return [{"appId": "1234-5678", "name": "TestApp"}]

    def get_onboarded_app(self, app_id: str) -> Dict:
        return {"appId": app_id, "name": "TestApp"}

    def delete_onboarded_app(self, app_id: str) -> None:
        print(f"Deleting application: {app_id}")

    def deploy_app(self, app_id: str, app_zones: List[Dict]) -> Dict:
        return {"appInstanceId": "abcd-efgh"}

    def get_all_deployed_apps(self, app_id: Optional[str] = None, app_instance_id: Optional[str] = None, region: Optional[str] = None) -> List[Dict]:
        return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    def undeploy_app(self, app_instance_id: str) -> None:
        print(f"Deleting app instance: {app_instance_id}")

    def get_edge_cloud_zones(self, region: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        logging.info('Contacting π-Edge...')
        nodes_response = requests.get('http://'+piedge_ip+'/piedge-connector/2.0.0/node')
        zone_list =[]
        if nodes_response.status_code==200:
            for node in nodes_response.json().get('nodes'):
                zone = {}
                zone['edgeCloudZoneId'] = node.get('uid')
                zone['edgeCloudZoneName'] = node.get('name')
                zone['edgeCloudZoneStatus'] = node.get('status')
                zone['edgeCloudProvider'] = edge_cloud_provider
                zone['edgeCloudRegion'] = node.get('location')
                zone_list.append(zone)
        return zone_list
