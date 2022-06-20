from typing import TypedDict

class access(TypedDict):
    configure: bool
    manage: bool
    view: bool


class Client(TypedDict):
    access: access
    alwaysDisplayInConsole: bool
    attributes: dict
    authenticationFlowBindingOverrides: dict
    baseUrl: str
    bearerOnly: bool
    clientAuthenticatorType: str
    clientId: str
    consentRequired: bool
    defaultClientScopes: list[str]
    defaultRoles: list[str]
    directAccessGrantsEnabled: bool
    enabled: bool
    frontchannelLogout: bool
    fullScopeAllowed: bool
    id: str
    implicitFlowEnabled: bool
    name: str
    nodeReRegistrationTimeout: int
    notBefore: int
    optionalClientScopes: list[str]
    protocol: str
    publicClient: bool
    redirectUris: list[str]
    rootUrl: str
    serviceAccountsEnabled: bool
    standardFlowEnabled: bool
    surrogateAuthRequired: bool
    webOrigins: list



