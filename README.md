TRIBES
======

TBP: General info on TRIBES and snakemake

# Getting started

*TRIBES* requires Linux-64 or MacOS-64 and about 10G of free disk space for software, reference and example data.

Setup tribes using one of the methods described in the [Installation] section 
(for local setup install with miniconda)

Create  and go to a directory for reference and sample data, e.g `$HOME/tribes-data`

	mkdir -p $HOME/tribes-data
	cd $HOME/tribes-data

Download and uncompress refecence data (4.3 GB) 

	wget https://s3-ap-southeast-2.amazonaws.com/csiro-tribes/downloads/reference/1.0/REF-G1K_EUR.tar.gz
	tar -xzf REF-G1K_EUR.tar.gz 
	rm REF-G1K_EUR.tar.gz  (optionally)

Download and uncompress example data (390 MB)

	wget https://s3-ap-southeast-2.amazonaws.com/csiro-tribes/downloads/examples/TFCeu.tar.gz
	tar -xzf TFCeu.tar.gz
	rm TFCeu.tar.gz  (optionally)


Go to your *TRIBES* installation directory and run *TRIBES* with:

	./tribes -d $HOME/tribes-data/TFCeu -j <no_cpu_cores> estimate_degree_vs_true

Where `no_cpu_cores` is the number of CPU core to use.

It takes about 20 minutes to to run the entire pipeline using 4 cores.

Upon the sucessful completion, you can find the final and intermediate stages of the pipeline in `$HOME/tribes-data/TFCeu/` (~2.3GB).
In particular:

- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_PH_GRM-allchr_FPI_IBD.csv` - includes the pairwise estimate of the degree of relatednes (`EstDegree`)
- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_PH_GRM-allchr_FPI_IBD_RVT.html` - notebook which compares estimated degrees vs the reported (true) ones.


The estimated relatedness is in CSV format with the following columns and data:

	Id1,Id2,IBD0.cM,IBD1.cM,IBD2.cM,EstDegree
	NA07347,NA11919,0.999073851764529,NA,NA,11
	NA12058,NA12829,0.999107459568523,NA,NA,11


To see the comparison results you can open the report in your preferred browser (e.g. `firefox`):

	firefox $HOME/tribes-data/TFCeu/TF-CEU-15-2_BiSnp_EurAF:0.01_LD_PH_GRM-allchr_FPI_IBD_RVT.html

The comparision is presented in the form of a dot chart like this:

![Dot plot estimated vs true](docs/assets/est_vs_true.png)

# Installation

TRIBES requires Linug-64 or MacOS-64

## Installation with miniconda 

Install `miniconda` from https://docs.conda.io/en/latest/miniconda.html  (does not matter which python version, I use the one for Python 2.7):

	wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
	sh Miniconda2-latest-Linux-x86_64.sh

Relogin to allow the changes in .bash_profile be activated.

Install dependencies for tribes (requries download of about 500 MB of software packages):

	./setup/install-with-conda.sh

This will create an conda environment named `tribes` and install all required dependencies, 
as well as create the appropriate TRIBES configuration file at `$HOME/.tribesrc`

## Manual installation

TRIBES requires 

	dplyr >= 0.8.0.1
	optparse >= 1.6.1 (1.3.2)
	rmarkdown >= 1.12 (!)
	ggplot >= 3.1.1 (2.2.1)

TBP: Complet dependencies and add reference to the requriements file.

## Cluster setup 

TBP: And reference to CSIRO setup readme (README-CSIRO.md)	

#Usage

## Preparing a custome pipelien


## Pipeline reference

TBP: The list of pipeline stages

# Datasets

TBD: Add info on datasets (REF and example)

















