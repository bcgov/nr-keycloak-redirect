"""pulls in env vars so they can be retrieved as app constants.

required env vars:
    KC_HOST            - the keycloak host
    KC_CLIENTID        - the keycloak client id that is configured with a
                         service account.
    KC_REALM           - the keycloak realm
    KC_SECRET          - secret used to authenticate service account against
                         keycloak
    KC_CLIENT_2_CONFIG - The key cloak client name that is being configured
                         ie the client who's redirect uri's will be added to
                         and removed by this app.
"""

import os
import dotenv
import sys
import logging

KC_HOST: str = ''
KC_CLIENTID: str = ''
KC_REALM: str = ''
KC_SECRET: str = ''
KC_CLIENT_2_CONFIG: str = ''

LOGGER = logging.getLogger(__name__)

envFile = '.env'

# populate the env vars from an .env file if it exists
envPath = os.path.join(os.path.dirname(__file__), '..', envFile)
localEnvPath = os.path.join(os.getcwd(), '.env')
LOGGER.debug(f"envPath: {envPath}")
if os.path.exists(envPath):
    LOGGER.debug(f"loading dot env {envPath}...")
    dotenv.load_dotenv(envPath)

elif os.path.exists(localEnvPath):
    LOGGER.debug(f"loading dot env {localEnvPath}...")
    dotenv.load_dotenv(localEnvPath)

# env vars that should be populated for script to run
ENV_VARS = ['KC_HOST', 'KC_CLIENTID', 'KC_REALM', 'KC_SECRET',
            'KC_CLIENT_2_CONFIG']
# KC_SA_CLIENTID

module = sys.modules[__name__]

envsNotSet = []
for env in ENV_VARS:
    if env not in os.environ:
        envsNotSet.append(env)
    else:
        # transfer env vars to module properties
        setattr(module, env, os.environ[env])

if envsNotSet:
    msg = 'The script expects the following environment variables to ' + \
          f'be set {envsNotSet}'
    raise EnvironmentError(msg)
