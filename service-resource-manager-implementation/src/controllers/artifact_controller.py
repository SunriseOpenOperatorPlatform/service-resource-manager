import logging
import json
import connexion
from src.models.copy_artifact_model import CopyArtifactModel
from src.models.artifact_exists_model import ArtifactExistsModel
from src.utils import artifact_connector

def artifact_exists():
    if connexion.request.is_json:
        try:
            # artifact = ArtifactExistsModel.from_dict(connexion.request.get_json())
            if connexion.request.get_json().get('registry_url') is None:
                return 'The registyr url must be provided', 400
            if connexion.request.get_json().get('artefact_name') is None:
                return 'Image name must be provided', 400
            response = artifact_connector.artifact_exists(connexion.request.get_json())
            return response.json()
        except Exception as e:
            logging.error(e.args)
            return e.args, 500
    else:
        return 'Request format must be JSON', 400

def copy_artifact():
    if connexion.request.is_json:
        try:
            artifact = CopyArtifactModel.from_dict(connexion.request.get_json())
            if artifact.dst_registry is None or artifact.src_registry is None:
                return 'The source and destination registries must be provided', 400
            if artifact.src_image_name is None:
                return 'The image name must be provided', 400
            response = artifact_connector.copy_artifact(artifact.to_dict())
            return response.json()
        except Exception as e:
            logging.error(e.args)
            return e.args
    else:
        return 'Request format must be JSON', 400