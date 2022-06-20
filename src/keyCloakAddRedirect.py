"""code required to add and remove redirect uri's to keycloak
"""

import logging
from typing import Optional, Union
import constants
import requests
import argparse
import sys
import validators
import kcTypes

LOGGER = logging.getLogger(__name__)


class ProcessArgs:

    def __init__(self) -> None:
        self.processArgs()

    def processArgs(self) -> None:
        parser = argparse.ArgumentParser(
            description='Add redirect url to forest client'
            )
        parser.add_argument(
            '-add', '--add-redirect-url', type=self.validUrl,
            help='define the redirect url you want to add')
        parser.add_argument(
            '-del', '--delete-redirect-url', type=self.validUrl,
            help='define the redirect url you want to remove')

        args = parser.parse_args()

        # deal if no args provided
        if not args.add_redirect_url and \
                not args.delete_redirect_url:
            parser.print_help()
            sys.exit()
        elif args.add_redirect_url:
            LOGGER.debug(f'adding redirect url: {args.add_redirect_url}')
            kc:KeyCloakClient = KeyCloakClient()
            kc.clientAddRedirect(args.add_redirect_url)

        elif args.delete_redirect_url:
            LOGGER.debug(f'removing redirect url: {args.delete_redirect_url}')
            kc = KeyCloakClient()
            kc.clientRemoveRedirect(args.delete_redirect_url)
        else:
            parser.print_help()

    def validUrl(self, url: str) -> str:
        if not validators.url(url):
            raise ValueError("invalid url")
        return url


class KeyCloakClient:

    def __init__(self) -> None:
        self.defaultHeaders = {'Accept': 'application/json'}
        self.access_token: str = ''

        self.getAccessToken()

    def getAccessToken(self) -> None:
        """using client id and secret queries keycloak for access token
        """
        uri = f"{constants.KC_HOST}/auth/realms/{constants.KC_REALM}" + \
              "/protocol/openid-connect/token"
        header = {'Accept': 'application/json'}
        params = {
                "client_id": constants.KC_CLIENTID,
                "client_secret": constants.KC_SECRET,
                "grant_type": "client_credentials"}
        LOGGER.debug(f'uri: {uri}')
        r = requests.post(uri, data=params, headers=header)
        r.raise_for_status()
        access_key = r.json()
        self.access_token = access_key['access_token']

    def getClients(self) -> list[kcTypes.Client]:
        '''
        Retrieves a list of the client objects from keycloak.
        '''
        Url = f"{constants.KC_HOST}/auth/admin/realms/" + \
                f"{constants.KC_REALM}/clients"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        response = requests.get(url=Url,
                                headers=headers
                                )
        response.raise_for_status()
        LOGGER.debug(f"response: {response.status_code}")

        data = response.json()
        return data

    def getClient(self, clientID: str) -> Union[kcTypes.Client, None]:
        """gets a list of all the clients in the realm and returns only the
        client that matches the clientID provided
        """
        clients = self.getClients()
        client = None
        for client in clients:
            if client['clientId'].lower() == clientID.lower():
                break
        return client

    def getClientDefinition(self) -> Union[kcTypes.Client, None]:
        """Retrieves the client definition that is defined in the variable:
        constants.KC_CLIENT_2_CONFIG

        :return: returns the client json structure for the client id defined
            in constants.KC_CLIENT_2_CONFIG
        :rtype: dict
        """
        client = self.getClient(constants.KC_CLIENT_2_CONFIG)
        if client:
            LOGGER.debug(f"clientid: {client['id']}")

            url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}" + \
                f"/clients/{client['id']}"  # noqa
            LOGGER.debug(f"uri is: {url}")

            headers = {
                "Authorization": "Bearer " + self.access_token,
                'Content-type': 'application/json',
                'Accept': 'application/json'}
            # TODO: could put in error checking... raise error if dont' get 200
            #       resp
            r = requests.get(url, headers=headers)
            client = r.json()
        return client

    def clientHasRedirectUri(self, redirect: str, client : Optional[kcTypes.Client] = None) -> bool: # noqa
        """returns a boolean indicating whether the supplied redirect url is
        defined as a redirect uri for the supplied client.

        if no client is supplied works on the client defined in the variable
        constants.KC_CLIENT_2_CONFIG

        :param redirect: the redirect url
        :type redirect: str
        :param client: client dict, defaults to None
        :type client: dict, optional
        :return: a boolean value indicating whether the supplied redirect url
            exists as a redirect url for the key cloak client
        :rtype: bool
        """
        #                body: Optional[list[str]] = None
        if client is None:
            client = self.getClient(constants.KC_CLIENT_2_CONFIG)
        returnVal = False
        # TODO: could add some intelligence here to for comparing the various
        #  redirect uri's
        if (client and  ('redirectUris' in client)) and \
                redirect.lower() in client['redirectUris']:
            returnVal = True
        return returnVal

    def addRedirectUri(self, client: kcTypes.Client, redirect: str) -> kcTypes.Client:
        """ adds a redirect url to the client, doesn't check to see if the url
        already exists or not.

        :param client: a dict describing the client
        :type client: dict
        :param redirect: the redirect url to be added to the client
        :type redirect: str
        :return: the client definition with the added redirect url
        :rtype: dict
        """
        if 'redirectUris' not in client:
            client['redirectUris'] = []
        client['redirectUris'].append(redirect)
        return client

    def deleteRedirectUri(self, client: kcTypes.Client, redirect: str) -> kcTypes.Client:
        """Looks for the redirect url in the client and if it exists then
        removes it

        :param client: a dict describing the client
        :type client: dict
        :param redirect: a redirect url
        :type redirect: str
        :return: the client definitions without the supplied redirect url
        :rtype: dict
        """
        LOGGER.debug(f"removing redirect if it exists: {redirect}")
        if 'redirectUris' in client:
            outputRedirects = []
            for redirectCurrent in client['redirectUris']:
                # todo: could create a specific method to determine if a url
                #       pattern matches, so that wildcard patterns would be
                #       evaluated etc.
                if redirectCurrent.lower() != redirect.lower():
                    outputRedirects.append(redirectCurrent)
                else:
                    LOGGER.debug("removing the redirect uri:" +
                                 f"{redirectCurrent}")
            client['redirectUris'] = outputRedirects
        return client

    def updateClientDefinition(self, clientJson: kcTypes.Client) -> None:
        """gets a client definition and updates the defined client in the api

        :param clientJson: the dict / json that is to be sent back to the
                           keycloak api
        :type clientJson: dict
        """
        url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientJson['id']}"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        r = requests.put(url, headers=headers, json=clientJson)
        LOGGER.debug(f"r status-code: {r.status_code}")
        LOGGER.debug(r)

    def clientAddRedirect(self, redirect:str) -> None:
        """ adds the redirect url to the client that who's name is defined in
        the parameter: constants.KC_CLIENT_2_CONFIG

        :param redirect: the redirect url to be added to the client
        :type redirect: str
        """
        client = self.getClient(constants.KC_CLIENT_2_CONFIG)
        if (client) and not self.clientHasRedirectUri(redirect, client=client):
            client = self.addRedirectUri(client, redirect)
            self.updateClientDefinition(client)

    def clientRemoveRedirect(self, redirect:str) -> None:
        """recieves the name of the redirect url that should be removed from the
        key cloak client

        :param redirect: name of the redirect uri
        :type redirect: str
        """
        client = self.getClient(constants.KC_CLIENT_2_CONFIG)
        if (client) and self.clientHasRedirectUri(redirect, client=client):
            client = self.deleteRedirectUri(client, redirect)
            self.updateClientDefinition(client)
        else:
            LOGGER.info(f"redirect URI: {redirect} was not found in client")



if __name__ == '__main__':

    LOGGER = logging.getLogger(__name__)
    LOGGER.setLevel(logging.DEBUG)
    hndlr = logging.StreamHandler()
    logstrdef = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d -' + \
                ' %(message)s'
    formatter = logging.Formatter(logstrdef)
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)
    LOGGER.debug("test")

    LOGGER.debug(f"KEYCLOAK client that is being configured: {constants.KC_CLIENT_2_CONFIG}") # noqa

    ProcessArgs()
