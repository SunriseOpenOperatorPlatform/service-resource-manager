# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.login_registration_request import LoginRegistrationRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLoginController(BaseTestCase):
    """LoginController integration test stubs"""

    def test_authentication_login(self):
        """Test case for authentication_login

        Login with a username and password.
        """
        body = LoginRegistrationRequest()
        response = self.client.open(
            '/piedge-connector/2.0.0/authentication',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
