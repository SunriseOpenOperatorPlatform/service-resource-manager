#!/usr/bin/env python3

import connexion

import logging
import sys
import os

from src import encoder

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main():
    global driver
    logging.basicConfig(level=logging.INFO)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', strict_validation=True, arguments={'title': 'π-edge Controller API'}, pythonic_params=True)
    app.run(port=8080)
    

if __name__ == '__main__':
    main()
