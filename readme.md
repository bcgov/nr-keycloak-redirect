# Add or Delete Redirect URIs in KeyCloak

BC Government pipelines frequently use ephemeral development environments that
differ by Pull Request number.  KeyCloak redirect URIs frequently need to be
revised to accommodate this.

## GitHub Action

Add a workflow to `.github/workflows/`.  At minimum the token/secret must be
stored as an Action or Environment variable.

### Workflow

```yaml
name: Pull Request

on:
  pull_request:
    branches:
      - main

jobs:
  keycloak-add:
    name: Add Redirect to Keycloak
    runs-on: ubuntu-latest
    steps:
      - name: Add
        uses: bcgov/nr-keycloak-redirect@main
        with:
          add_delete: 'add'
          redirect: 'https://google.com'
          secret: ${{ secrets.KC_SECRET }}
          clientid : ${{ secrets.KC_CLIENTID }}
          clientid_2: 'fom'
          realm: ${{ secrets.KC_REALM }}
          host: ${{ secrets.KC_HOST }}
```

### Parameters

 - add_delete: [add|del]
 - redirect: redirect URI, e.g. https://<WHATEVER>.apps.silver.devops.gov.bc.ca/*
 - secret: client secret
 - clientid: client to authenticate from
 - clientid_2: client to apply changes to
 - realm: Keycloak custom realm, e.g. abcd1234
 - host: Keycloak host, e.g. https://server.ca

## Local install

### setup - install deps

```
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### setup - define env vars

Define the following environment variables:

```
KC_HOST=<keycloak host>
KC_CLIENTID=<keycloak client id with service account>
KC_SECRET=<keycloak secret>
KC_REALM=<keycloak realm>
KC_CLIENT_2_CONFIG=<keycloak client who's redirect urls are to be modified>
```

### Add Redirect:

`python src/keyCloakAddRedirect.py -add redirect_url`

### Remove Redirect:
`python src/keyCloakAddRedirect.py -del redirect_url`

