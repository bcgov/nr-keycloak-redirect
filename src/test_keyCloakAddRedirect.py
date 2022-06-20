

import logging
import keyCloakAddRedirect
import pprint
import kcTypes

import pytest

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")

PP  = pprint.PrettyPrinter(indent=4)

class Test_KeyCloakClient:

    def test_getAccessToken(self, keyCloakClient: keyCloakAddRedirect.KeyCloakClient) -> None:
        keyCloakClient.getAccessToken()
        LOGGER.debug("debug message test")
        assert keyCloakClient.access_token

    def test_getClients(self, keyCloakClient: keyCloakAddRedirect.KeyCloakClient) -> None:
        clients = keyCloakClient.getClients()
        clientsStr = PP.pformat(clients)
        LOGGER.debug(clientsStr)



@pytest.fixture
def keyCloakClient() -> keyCloakAddRedirect.KeyCloakClient:
    return keyCloakAddRedirect.KeyCloakClient()
