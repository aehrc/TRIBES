TRIBES
======

This section is specific to setting up and running TRIBES in CSIRO HPC cluster pearcey.
It can be used as reference for runnign tribes in other cluster environments.


CSIRO HPC cluster is running 20CPU 128GB nodes with `slurm` as scheduler and `env modulules` to support versioning of tools and applications. 

## Setting up on pearcey 

This is CSIRO internal setup, but in the futre will be extened to support 
non CSIRO environments.

Perform the following installation setps.

* install snakemake>=5.4 with in python 3.6.1 
* install tribes.tools R package from sources in R/3.5.0

E.g:

	module load python/3.6.1
	pip install --user --upgrade 'snakemake>=5.4'


	module load R/3.5.0
	R --no-save

	>> in R shell type

	install.packages('R/tribes.tools', repos=NULL, type='source')

	>> then agree to create a user library

Configure tribes:

	cp setup/pearcey/tribesrc ~/.tribesrc
	mkdir -p ~/.config/snakemake/cluster
	cp setup/pearcey/cluster.config.yaml ~/.config/snakemake/cluster/config.yaml

## Running examples on pearcey

ssh to one of the pearcey interactive nodes e.g. `pearcey-i1.hpc.csiro.au`.

Select working directory for the sample dataset e.g. `/flush3/$USER/TFCeu`

Copy the example dataset with configuration from `/flush2/projects/HB_TB_Share/TRIBES/samples/TFCeu` to your working dir.

	cp -r /flush2/projects/HB_TB_Share/TRIBES/samples/TFCeu /flush3/$USER/TFCeu

To run TRIBES (estimate relatedness) locally using 4 CPU cores:

	./tribes -d /flush3/$USER/TFCeu --cores 4 estimate_degree

To run TRIBES using slurm:

	./tribes -d /flush3/$USER/TFCeu --profile cluster estimate_degree

To generate report comparing the estimated relatendess against the reported relations:

	./tribes -d /flush3/$USER/TFCeu --profile cluster estimate_degree_vs_true


The results are in the working dir `/flush3/$USER/TFCeu`:

- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_GRM-allchr_IBD.csv` - estimated IBD0 and EstimatedDegree
- `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_GRM-allchr_IBD_RVT.html` - comparision agains reported relatedness








