#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Copyright 2025-present by Software Networks Area, i2CAT.
# All rights reserved.
#
# This file is part of the Open SDK
#
# Contributors:
#   - Adrián Pino Martínez (adrian.pino@i2cat.net)
#   - Sergio Giménez (sergio.gimenez@i2cat.net)
##
from typing import Dict, List, Optional

from src import logger
from src.edgecloud.core.edgecloud_interface import EdgeCloudManagementInterface

from . import schemas
from .common import (
    I2EdgeError,
    i2edge_delete,
    i2edge_get,
    i2edge_post,
    i2edge_post_multiform_data,
)

log = logger.get_logger(__name__)


class EdgeApplicationManager(EdgeCloudManagementInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_edge_cloud_zones(
        self, region: Optional[str] = None, status: Optional[str] = None
    ) -> list[dict]:
        url = "{}/zones/list".format(self.base_url)
        params = {}
        try:
            response = i2edge_get(url, params=params)
            log.info("Availability zones retrieved successfully")
            return response
        except I2EdgeError as e:
            raise e

    # Harcoded
    def get_edge_cloud_zones_details(
        self, zone_id: str, flavour_id: Optional[str] = None
    ) -> Dict:
        # Minimal mocked response based on required fields of 'ZoneRegisteredData' in GSMA OPG E/WBI API
        return {
            "zoneId": zone_id,
            "reservedComputeResources": [
                {
                    "cpuArchType": "ISA_X86_64",
                    "numCPU": "4",
                    "memory": 8192,
                }
            ],
            "computeResourceQuotaLimits": [
                {
                    "cpuArchType": "ISA_X86_64",
                    "numCPU": "8",
                    "memory": 16384,
                }
            ],
            "flavoursSupported": [
                {
                    "flavourId": "medium-x86",
                    "cpuArchType": "ISA_X86_64",
                    "supportedOSTypes": [
                        {
                            "architecture": "x86_64",
                            "distribution": "UBUNTU",
                            "version": "OS_VERSION_UBUNTU_2204_LTS",
                            "license": "OS_LICENSE_TYPE_FREE",
                        }
                    ],
                    "numCPU": 4,
                    "memorySize": 8192,
                    "storageSize": 100,
                }
            ],
        }

    def _create_artefact(
        self,
        artefact_id: str,
        artefact_name: str,
        repo_name: str,
        repo_type: str,
        repo_url: str,
        password: Optional[str] = None,
        token: Optional[str] = None,
        user_name: Optional[str] = None,
    ):
        repo_type = schemas.RepoType(repo_type)
        url = "{}/artefact".format(self.base_url)
        payload = schemas.ArtefactOnboarding(
            artefact_id=artefact_id,
            name=artefact_name,
            repo_password=password,
            repo_name=repo_name,
            repo_type=repo_type,
            repo_url=repo_url,
            repo_token=token,
            repo_user_name=user_name,
        )
        try:
            i2edge_post_multiform_data(url, payload)
            log.info("Artifact added successfully")
        except I2EdgeError as e:
            raise e

    def _get_artefact(self, artefact_id: str) -> Dict:
        url = "{}/artefact/{}".format(self.base_url, artefact_id)
        try:
            response = i2edge_get(url, artefact_id)
            log.info("Artifact retrieved successfully")
            return response
        except I2EdgeError as e:
            raise e

    def _get_all_artefacts(self) -> List[Dict]:
        url = "{}/artefact".format(self.base_url)
        try:
            response = i2edge_get(url, {})
            log.info("Artifacts retrieved successfully")
            return response
        except I2EdgeError as e:
            raise e

    def _delete_artefact(self, artefact_id: str):
        url = "{}/artefact".format(self.base_url)
        try:
            i2edge_delete(url, artefact_id)
            log.info("Artifact deleted successfully")
        except I2EdgeError as e:
            raise e

    def onboard_app(self, app_manifest: Dict) -> Dict:
        try:
            app_id = app_manifest["appId"]
            artefact_id = app_id

            app_component_spec = schemas.AppComponentSpec(artefactId=artefact_id)
            data = schemas.ApplicationOnboardingData(
                app_id=app_id, appComponentSpecs=[app_component_spec]
            )
            payload = schemas.ApplicationOnboardingRequest(profile_data=data)
            url = "{}/application/onboarding".format(self.base_url)
            i2edge_post(url, payload)
        except I2EdgeError as e:
            raise e
        except KeyError as e:
            raise I2EdgeError("Missing required field in app_manifest: {}".format(e))

    def delete_onboarded_app(self, app_id: str) -> None:
        url = "{}/application/onboarding".format(self.base_url)
        try:
            i2edge_delete(url, app_id)
        except I2EdgeError as e:
            raise e

    def get_onboarded_app(self, app_id: str) -> Dict:
        url = "{}/application/onboarding/{}".format(self.base_url, app_id)
        try:
            response = i2edge_get(url, app_id)
            return response
        except I2EdgeError as e:
            raise e

    def get_all_onboarded_apps(self) -> List[Dict]:
        url = "{}/applications/onboarding".format(self.base_url)
        params = {}
        try:
            response = i2edge_get(url, params)
            return response
        except I2EdgeError as e:
            raise e

    # Harcoded
    def deploy_app(self, app_id: str, app_zones: List[Dict]) -> Dict:
        return {"appInstanceId": "abcd-efgh"}

    # Harcoded
    def get_all_deployed_apps(
        self,
        app_id: Optional[str] = None,
        app_instance_id: Optional[str] = None,
        region: Optional[str] = None,
    ) -> List[Dict]:
        return [{"appInstanceId": "abcd-efgh", "status": "ready"}]

    # Harcoded
    def undeploy_app(self, app_instance_id: str) -> None:
        print(f"Deleting app instance: {app_instance_id}")
