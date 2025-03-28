# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.apps_response import AppsResponse  # noqa: E501
from swagger_server.models.apps_response_apps import AppsResponseApps  # noqa: E501
from swagger_server.models.service_function_registration_request import ServiceFunctionRegistrationRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServiceFunctionsCatalogueController(BaseTestCase):
    """ServiceFunctionsCatalogueController integration test stubs"""

    def test_deregister_service_function(self):
        """Test case for deregister_service_function

        Deregister service.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deregisterServiceFunction/{serviceFunctionName}'.format(service_function_name='service_function_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_service_function(self):
        """Test case for get_service_function

        Returns a specific service function from the catalogue.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/serviceFunctions/{serviceFunctionId}'.format(service_function_id='service_function_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_service_functions(self):
        """Test case for get_service_functions

        Returns service functions from the catalogue.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/serviceFunctions',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_service_function(self):
        """Test case for register_service_function

        Register Service.
        """
        body = ServiceFunctionRegistrationRequest()
        response = self.client.open(
            '/piedge-connector/2.0.0/registerServiceFunction',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_service_function(self):
        """Test case for update_service_function

        Update Service registration.
        """
        body = ServiceFunctionRegistrationRequest()
        response = self.client.open(
            '/piedge-connector/2.0.0/updateServiceFunction',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
