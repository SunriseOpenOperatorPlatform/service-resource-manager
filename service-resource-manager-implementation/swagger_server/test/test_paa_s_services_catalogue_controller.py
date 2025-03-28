# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.apps_response import AppsResponse  # noqa: E501
from swagger_server.models.apps_response_apps import AppsResponseApps  # noqa: E501
from swagger_server.models.paas_registration_request import PaasRegistrationRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPaaSServicesCatalogueController(BaseTestCase):
    """PaaSServicesCatalogueController integration test stubs"""

    def test_deregister_paas(self):
        """Test case for deregister_paas

        Deregister PaaS.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deregisterPaas/{paasServiceName}'.format(paas_service_name='paas_service_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_paas_services(self):
        """Test case for get_paas_services

        Returns PaaS Services from the catalogue.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/paasServices',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_pas_service(self):
        """Test case for get_pas_service

        Returns a specific PaaS service from the catalogue.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/paasServices/{paasServiceId}'.format(paas_service_id='paas_service_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_paas(self):
        """Test case for register_paas

        Register PaaS.
        """
        body = PaasRegistrationRequest()
        response = self.client.open(
            '/piedge-connector/2.0.0/registerPaas',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_paas(self):
        """Test case for update_paas

        Update PaaS registration.
        """
        body = PaasRegistrationRequest()
        response = self.client.open(
            '/piedge-connector/2.0.0/updatePaas',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
