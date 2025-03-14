import logging
import json
import connexion
from swagger_server.models.copy_artifact_model import CopyArtifactModel
from swagger_server.models.artifact_exists_model import ArtifactExistsModel
from swagger_server.services import artifact_service

def artifact_exists(body):
    if connexion.request.is_json:
        try:
            artifact = ArtifactExistsModel.from_dict(body)
            if artifact.registry_url is None:
                return 'The registyr url must be provided', 400
            if artifact.image_name is None:
                return 'Image name must be provided', 400
            response = artifact_service.artifact_exists(artifact)
            return response
        except Exception as e:
            logging.error(e.args)
            return e.args, 500
    else:
        return 'Request format must be JSON', 400

def copy_artifact(body):
    if connexion.request.is_json:
        try:
            artifact = CopyArtifactModel.from_dict(body)
            if artifact.dst_registry is None or artifact.src_registry is None:
                return 'The source and destination registries must be provided', 400
            if artifact.src_image_name is None:
                return 'The image name must be provided', 400
            response = artifact_service.copy_artifact(artifact)
            return response
        except Exception as e:
            logging.error(e.args)
            return e.args
    else:
        return 'Request format must be JSON', 400