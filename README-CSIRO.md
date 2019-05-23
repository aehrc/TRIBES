TRIBES
======

This section is specific to setting up and running TRIBES in CSIRO HPC cluster pearcey.
It can be used as reference for runnign tribes in other cluster environments.


CSIRO HPC cluster is running 20CPU 128GB nodes with `slurm` as scheduler and `env modulules` to support versioning of tools and applications. 

# Setup


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

ssh to one of the pearcey interactive nodes e.g. `pearcey-i1.hpc.csiro.au`.

Activate tribes conda environment (see above:)

	conda activate tribes

Select working directory for the sample dataset e.g. `/flush3/$USER/TFCeu`

Copy the example dataset with configuration from `/flush2/projects/HB_TB_Share/TRIBES/samples/TFCeu` to your working dir.

	cp -r /flush2/projects/HB_TB_Share/TRIBES/samples/TFCeu /flush3/$USER/TFCeu

To run TRIBES (estimate relatedness) locally using 4 CPU cores:

	./sn -d /flush3/$USER/TFCeu --cores 4

To run TRIBES using slurm:

	./sn-cluster -d /flush3/$USER/TFCeu


To generate report comparing the estimated relatendess against the reported relations:

	./sn-cluster -d /flush3/$USER/TFCeu estimate_degree_vs_true


The results are in the working dir `/flush3/$USER/TFCeu`:

- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_GRM-allchr_IBD.csv` - estimated IBD0 and EstimatedDegree
- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_GRM-allchr_IBD_RVT.html` - comparision agains reported relatedness








