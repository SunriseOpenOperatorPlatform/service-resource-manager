# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.deploy_chain import DeployChain  # noqa: E501
from swagger_server.models.deploy_service_function import DeployServiceFunction  # noqa: E501
from swagger_server.models.deployedapps_response import DeployedappsResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServiceFunctionsInstancesController(BaseTestCase):
    """ServiceFunctionsInstancesController integration test stubs"""

    def test_delete_chain(self):
        """Test case for delete_chain

        Deletes a deployed chain.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deleteChain/{chainServiceName}'.format(chain_service_name='chain_service_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_deployed_service_function(self):
        """Test case for delete_deployed_service_function

        Deletes a deployed Service function.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deletedeployedServiceFunction/{deployedServiceFunctionName}'.format(deployed_service_function_name='deployed_service_function_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deploy_chain(self):
        """Test case for deploy_chain

        Request to deploy a chain of function services.
        """
        body = DeployChain()
        response = self.client.open(
            '/piedge-connector/2.0.0/deployChain',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deploy_service_function(self):
        """Test case for deploy_service_function

        Request to deploy a Service function (from the catalogue) to an edge node.
        """
        body = DeployServiceFunction()
        response = self.client.open(
            '/piedge-connector/2.0.0/deployServiceFunction',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deployed_service_function_status(self):
        """Test case for deployed_service_function_status

        Returns the requested edge service status per node.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deployedServiceFunctions/{deployedServiceFunctionName}'.format(deployed_service_function_name='deployed_service_function_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deployed_service_functions_status(self):
        """Test case for deployed_service_functions_status

        Returns the edge service functions status per node.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deployedServiceFunctions',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_chain(self):
        """Test case for update_chain

        Request to update a chain of function services.
        """
        body = DeployChain()
        response = self.client.open(
            '/piedge-connector/2.0.0/updateChain',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_deployed_service_function(self):
        """Test case for update_deployed_service_function

        Request to update the status of a service.
        """
        body = DeployServiceFunction()
        response = self.client.open(
            '/piedge-connector/2.0.0/updateDeployedServiceFunction',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
