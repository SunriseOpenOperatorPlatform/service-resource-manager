# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.deploy_chain import DeployChain  # noqa: E501
from swagger_server.models.deploy_paas import DeployPaas  # noqa: E501
from swagger_server.models.deployedapps_response import DeployedappsResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPaaSServicesInstancesController(BaseTestCase):
    """PaaSServicesInstancesController integration test stubs"""

    def test_delete_deployed_paas_service(self):
        """Test case for delete_deployed_paas_service

        Deletes a deployed PaaS service.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deletedeployedPaas/{deployedPaasServiceName}:'.format(deployed_paas_service_name='deployed_paas_service_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deploy_paas(self):
        """Test case for deploy_paas

        Request to deploy a PaaS (from the catalogue) to an edge node.
        """
        body = DeployPaas()
        response = self.client.open(
            '/piedge-connector/2.0.0/deployPaas',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deployed_paas_service_status(self):
        """Test case for deployed_paas_service_status

        Returns the requested edge paas service status.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deployedPaasServices/{deployedPaasServiceName}'.format(deployed_paas_service_name='deployed_paas_service_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deployed_paas_services_status(self):
        """Test case for deployed_paas_services_status

        Returns edge paas services status.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deployedPaas',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_deployed_paas(self):
        """Test case for update_deployed_paas

        Request to update the status of a deployed PaaS.
        """
        body = DeployChain()
        response = self.client.open(
            '/piedge-connector/2.0.0/updateDeployedPaas',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
