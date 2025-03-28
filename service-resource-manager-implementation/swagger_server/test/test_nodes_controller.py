# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.deploy_paa_s_node import DeployPaaSNode  # noqa: E501
from swagger_server.models.nodes_response import NodesResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNodesController(BaseTestCase):
    """NodesController integration test stubs"""

    def test_activate_paas_node(self):
        """Test case for activate_paas_node

        Request to create a \"PaaS-enabled\" node.
        """
        body = DeployPaaSNode()
        response = self.client.open(
            '/piedge-connector/2.0.0/activatePaasNode',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_nodes(self):
        """Test case for get_nodes

        Returns the edge nodes status.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/nodes',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_init_nodes(self):
        """Test case for init_nodes

        Initiliaze nodes. Scan nodes in the edge cluster.
        """
        response = self.client.open(
            '/piedge-connector/2.0.0/initNodes',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
