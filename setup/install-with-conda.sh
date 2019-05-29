#!/bin/bash
set -e

PWD=$(cd "`dirname $0`"/..; pwd)
TRIBES_ENV=tribes
CONDA_ACTIVATE="conda"
if [ -n "$(which activate 2> /dev/null; echo -n)" ]; then
    CONDA_ACTIVATE="source"
fi
echo $CONDA_ACTIVATE
conda env create --force -n ${TRIBES_ENV} -f "${PWD}/setup/environment.yaml"
${CONDA_ACTIVATE} activate ${TRIBES_ENV}
Rscript --vanilla -e "install.packages('${PWD}/R/tribes.tools',repos=NULL)"
cat > "${HOME}/.tribesrc" <<EOF
${CONDA_ACTIVATE} activate ${TRIBES_ENV}
EOF
