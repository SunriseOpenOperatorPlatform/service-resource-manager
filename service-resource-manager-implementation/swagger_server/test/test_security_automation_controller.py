# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.activate_secured_slice import ActivateSecuredSlice  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSecurityAutomationController(BaseTestCase):
    """SecurityAutomationController integration test stubs"""

    def test_activate_secured_slice(self):
        """Test case for activate_secured_slice

        Enables a secured slice
        """
        body = ActivateSecuredSlice()
        response = self.client.open(
            '/piedge-connector/2.0.0/activateSecuredSlice',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_secured_slice(self):
        """Test case for delete_secured_slice

        Disables security monitoring over a slice
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/deactivateSecuredSlice/{sliceName}'.format(slice_name='slice_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
