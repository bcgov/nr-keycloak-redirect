#!/bin/bash

# Required envars
vars=(
    "KC_HOST"
    "KC_CLIENTID"
    "KC_SECRET"
    "KC_REALM"
    "KC_CLIENT_2_CONFIG"
)

# Check envars
fail="false"
for v in ${vars[@]}; do
    if [ -z "${!v}" ]; then
        echo "ERROR: ${v} is not set"
        fail="true"
    else
        export ${v}=${!v}
    fi
done

# Handle result
if [ "${fail}" == "true" ]; then
    echo "Exiting due to missing environment variables"
    exit 1
fi

# Script body
set -euo pipefail

# Very the correct number of params and provide output
THIS_FILE="$(dirname ${0})/$(basename ${0})"
[ "${#}" -eq 2 ] || {
    echo -e "\nUsage: ${THIS_FILE} [add|remove] <redirect_url>\n"
	exit
}
CMD=${1}
URL=${2}

# Run command
python src/keyCloakAddRedirect.py -${CMD} ${URL}
