#!/bin/bash
set -e

PWD=$(cd "`dirname $0`"/..; pwd)
TRIBES_ENV=tribes

conda create -y -n ${TRIBES_ENV} python=3.6
source activate ${TRIBES_ENV}
conda install -y --clobber -c conda-forge -c bioconda -c aehrc --file "${PWD}/setup/requirements.txt"
pip install 'snakemake>=5.4'
Rscript --vanilla -e "install.packages('${PWD}/R/tribes.tools',repos=NULL)"
cat > "${HOME}/.tribesrc" <<EOF
source activate ${TRIBES_ENV}
EOF
