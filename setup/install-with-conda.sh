#!/usr/bin/env bash
set -e

[ -d "$HOME/miniconda" ] && CONDA_BASE=$HOME/miniconda
[ -d "$HOME/miniconda3" ] && CONDA_BASE=$HOME/miniconda3
[ -f `which conda` ] && CONDA_BASE="$(conda info --base)"

if [ -z "$CONDA_BASE" ]
then
    echo "Could not locate Miniconda in PATH or default directories."
    exit 1
else
    echo "Using Miniconda installation: $CONDA_BASE"
fi

TRIBES_ENV=tribes
${CONDA_BASE}/bin/conda env create -n ${TRIBES_ENV} -f setup/environment.yaml
source "${CONDA_BASE}/bin/activate" ${TRIBES_ENV}
Rscript --vanilla -e "install.packages('R/tribes.tools',repos=NULL)"
cat > "${HOME}/.tribesrc" <<EOF
source "${CONDA_BASE}/bin/activate" ${TRIBES_ENV}
EOF
