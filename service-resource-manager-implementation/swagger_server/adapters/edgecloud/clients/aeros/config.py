##
# This file is part of the Open SDK
#
# Contributors:
#   - Vasilis Pitsilis (vpitsilis@dat.demokritos.gr, vpitsilis@iit.demokritos.gr)
#   - Andreas Sakellaropoulos (asakellaropoulos@iit.demokritos.gr)
##
"""
aerOS access configuration
Access tokens need to be provided in environment variables.
"""
import os

aerOS_API_URL = os.environ.get("aerOS_API_URL")
if not aerOS_API_URL:
    raise ValueError("Environment variable 'aerOS_API_URL' is not set.")
aerOS_ACCESS_TOKEN = os.environ.get("aerOS_ACCESS_TOKEN")
if not aerOS_ACCESS_TOKEN:
    raise ValueError("Environment variable 'aerOS_ACCESS_TOKEN' is not set.")
aerOS_HLO_TOKEN = os.environ.get("aerOS_HLO_TOKEN")
if not aerOS_HLO_TOKEN:
    raise ValueError("Environment variable 'aerOS_HLO_TOKEN' is not set.")
DEBUG = True
LOG_FILE = ".log/aeros_client.log"
