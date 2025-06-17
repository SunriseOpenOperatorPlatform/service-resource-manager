import logging
import requests
import os
import json

artifact_manager_ip = os.environ['ARTIFACT_MANAGER_ADDRESS']

def artifact_exists(body):
    logging.info('Contacting Artifact Manager')
    body = json.dumps(body)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://'+artifact_manager_ip+'/artefact-exists/', headers=headers, json=body)
    return response

def copy_artifact(body):
    logging.info('Submitting artifact to Artifact Manager')
    body = json.dumps(body)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://'+artifact_manager_ip+'/copy-artefact', headers=headers, json=body)
    return response