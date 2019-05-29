#!/bin/bash
set -e

PWD=$(cd "`dirname $0`"/..; pwd)
TRIBES_ENV=tribes
conda env create --force -n ${TRIBES_ENV} -f "${PWD}/setup/environment.yaml"
source activate ${TRIBES_ENV}
Rscript --vanilla -e "install.packages('${PWD}/R/tribes.tools',repos=NULL)"
cat > "${HOME}/.tribesrc" <<EOF
source activate ${TRIBES_ENV}
EOF
