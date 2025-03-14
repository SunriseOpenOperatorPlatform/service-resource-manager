from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401
from typing import List, Dict

from swagger_server.models.base_model_ import Model
from swagger_server import util

class ArtifactExistsModel(Model):

    def __init__(self, registry_url : str, image_name: str, image_tag: str=None, username: str=None, password: str=None):

        self.swagger_types = {
            'registry_url': str,
            'image_name': str,
            'image_tag': str,
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'registry_url': 'registry_url',
            'image_name': 'image_name',
            'image_tag': 'image_tag',
            'username': 'username',
            'password': 'password'
        }
        self._registry_url = registry_url
        self._image_name = image_name
        self._image_tag = image_tag
        self._username = username
        self._password = password


    @classmethod
    def from_dict(cls, dikt) -> 'ArtifactExistsModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CopyArtifactModel.  # noqa: E501
        :rtype: CopyArtifactModel
        """
        return util.deserialize_model(dikt, cls)
    
    @property
    def registry_url(self) -> str:
        """Gets the registry_url of this ArtifactExistsModel.

        :return: The registry_url of this ArtifactExistsModel.
        :rtype: str
        """
        return self._registry_url

    @registry_url.setter
    def registry_url(self, registry_url: str):
        """Sets the registry_url of this ArtifactExistsModel.

        :param name: The registry_url of this ArtifactExistsModel.
        :type name: str
        """

        self._registry_url = registry_url


    @property
    def image_name(self) -> str:
        """Gets the image_name of this ArtifactExistsModel.

        :return: The image_name of this ArtifactExistsModel.
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name: str):
        """Sets the image_name of this ArtifactExistsModel.

        :param name: The image_name of this ArtifactExistsModel.
        :type name: str
        """

        self._image_name = image_name

    @property
    def image_tag(self) -> str:
        """Gets the image_tag of this ArtifactExistsModel.

        :return: The image_tag of this ArtifactExistsModel.
        :rtype: str
        """
        return self._image_tag

    @image_tag.setter
    def image_tag(self, image_tag: str):
        """Sets the image_tag of this ArtifactExistsModel.

        :param name: The image_tag of this ArtifactExistsModel.
        :type name: str
        """

        self._image_tag = image_tag

    @property
    def username(self) -> str:
        """Gets the username of this ArtifactExistsModel.

        :return: The username of this ArtifactExistsModel.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this ArtifactExistsModel.

        :param name: The username of this ArtifactExistsModel.
        :type name: str
        """

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this ArtifactExistsModel.

        :return: The password of this ArtifactExistsModel.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this ArtifactExistsModel.

        :param name: The password of this ArtifactExistsModel.
        :type name: str
        """

        self._password = password   