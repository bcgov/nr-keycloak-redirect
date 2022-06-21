#!/bin/bash
#
set -euo pipefail

# Receive parameters
ADD_DEL=${1}
REDIRECT=${2}

# Envars
export KC_SECRET=${3}
export KC_CLIENT=${4}
export KC_CLIENT_2_CONFIG=${5}
export KC_REALM=${6}
export KC_HOST=${7}

# Run command
python src/keyCloakAddRedirect.py -${ADD_DEL} ${REDIRECT}
