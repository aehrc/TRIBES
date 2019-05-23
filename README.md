TRIBES
======

# Usage


## Installation

TRIBES requires 


dplyr >= 0.8.0.1
optparse >= 1.6.1 (1.3.2)
rmarkdown >= 1.12 (!)
ggplot >= 3.1.1 (2.2.1)


## Setting up on pearcey 

This is CSIRO internal setup, but in the futre will be extened to support 
non CSIRO environments.

Install `miniconda` from https://docs.conda.io/en/latest/miniconda.html  

- Does not matter which python version, I use the one for Python 2.7)
- Since the quota on $HOME is very small install miniconda in `/flush1/$USER/miniconda2`.

E.g:

	wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
	sh Miniconda2-latest-Linux-x86_64.sh -p /flush1/$USER/miniconda2

Relogin to allow the changes in .bash_profile be activated.

Create and activate the enviroment for TRIBES (e.g. named `tribes`) with python 3.6

	conda create -n tribes python=3.6
	conda activate tribes

Install the required python and R packages:

	conda install --file setup/requirements.txt

Perform additional installation steps:

* install snakemake with pip 
* install tribes.tools R package from sources

E.g:

	pip install snakemake
	Rscript --vanilla -e "install.packages('R/tribes.tools', repos=NULL)"

Done!



# Examples


## Running examples on pearcey








