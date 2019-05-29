TRIBES
======

TBP: General info on *TRIBES* and snakemake

# Getting started

*TRIBES* requires Linux-64 or MacOS-64 and about 10G of free disk space for software, reference and example data.

Setup *TRIBES* using one of the methods described in the [Installation](#installation) section 
(for a workstation setup use: [Installation with miniconda](#installation-with-miniconda) )

To demonstate how tribes works we will use on of the examples (TFCeu) with reference data from EUR superpopulation (REF-G1K_EUR).

Create  and go to a directory for reference and sample data, e.g `$HOME/tribes-data`

	mkdir -p $HOME/tribes-data
	cd $HOME/tribes-data

Download and uncompress refecence data (4.3 GB) 

	wget https://s3-ap-southeast-2.amazonaws.com/csiro-tribes/downloads/reference/1.0/REF-G1K_EUR.tar.gz
	tar -xzf REF-G1K_EUR.tar.gz 
	rm REF-G1K_EUR.tar.gz  (optionally)

The reference data is subset of 1000 genomes dataset with unrelated EUR inviduals and it's used in various stages of preprocessing (e.g. LD prunning, phasing or filtering on MAF).

Download and uncompress example data (390 MB)

	wget https://s3-ap-southeast-2.amazonaws.com/csiro-tribes/downloads/examples/TFCeu.tar.gz
	tar -xzf TFCeu.tar.gz
	rm TFCeu.tar.gz  (optionally)

The sample data is a synhtetic pedigee created from unrelated CEU individuals. 
For more info on the dataset see the [Datasets](#datasets) section. Inside the `TFCeu` directory you will find the following files:

- `TF-CEU-15-2.vcf.gz` - the source multisample VCF files
- `TF-CEU-15-2.true.rel` - the true pariwise relations
- `g1k_ceu_family_15_2.ped` - pedigee
- `config.yaml` - the configuration file for *TRIBES* pipeline.  

The `config.yaml` provideds configuration for the pipeline defining the location and name of reference data and the true relations file, as well as the name of the imput file and the preprocessing steps required before IBD/relatedness estimation, e.g.:

	rel_sample: "TF-CEU-15-2_BiSnp_EurAF:0.01_LD"

identifies `TF-CEU-15.vcf.gz` as the input file and applies pre-processing that includes filtering on biallelic SNPs and MAF and LD prunning.

Note: Please not that the IBD estimation requires a phased VCF file. If the input file is not phased pre-processing must include phasing (usually las the last step),  e.g. `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_PH` (to phase without reference) or `TF-CEU-15-2_BiSnp_EurAF:0.01_LD_RPH` (to phase with reference). This is not required in this example becasue the input VCF is phased.

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

Read the secions below to find out how to setup and configure a pipline on your data.

# Installation

TRIBES requires Linux-64 or MacOS-64.

Download the latest release of *TRIBES* from https://github.com/aehrc/TRIBES/releases
and uncompress it to your selected directory.

Alternatively you can clone the (unstable) most recent version from github: 

	git clone https://github.com/aehrc/TRIBES.git

## Installation with miniconda 

Install `miniconda` from https://docs.conda.io/en/latest/miniconda.html  (does not matter which python version, I use the one for Python 2.7):

	wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
	sh Miniconda2-latest-Linux-x86_64.sh

Relogin to allow the changes in `.bash_profile` be activated.

Go to the *TRIBES* instalation directory.

Install dependencies for tribes (requries download of about 500 MB of software packages):

	./setup/install-with-conda.sh

This will create an conda environment named `tribes` and install all required dependencies, 
as well as create the appropriate *TRIBES *configuration file at `$HOME/.tribesrc`

To check the installation run:

	./tribes 

This should display amongs others usage info.

## Manual installation

*TRIBES* is implemented as a `snakemake` pipeline and relies a number of bioinformatics tools for processing, such as `bcftools`, `bgzip`, `tabix`, `vcftools`, `germline`, `beagle` as well as a number of `python` an `R` packages.

The complete list of dependencies and their required (minimal) versions can be inferred from the conda environment file at: [setup/environment.yaml](setup/environment.yaml)

They can be installed using the OS specific way (e.g. using `apt` or `yum` on Linxu or `brew` on MacOS)

In addition *TRIBES* requires `tribes.tools` `R` packages which can be installed from souces with:

	Rscript --vanilla -e "install.packages('R/tribes.tools',repos=NULL)"

## Cluster setup 

`snakemake` and thus *TRIBES* can run on HPC clusters (for example with `slurm`).

An example setup for CSIRO HPC cluster is descibed in [README-CSIRO.md](README-CSIRO.md) and can be used as a guide 
to configure *TRIBES* on other clusters. 

For more information on running `snakemake` on HPC clusters please check the `snakemake` documentation.

#Usage

## Preparing a custome pipelien


## Pipeline reference

The following steps can used in the pipeline.

Preprocessing:

- `NM`: retain only loci with with non-missing genotypes
- `BiSnp` : retain only bi-allelic SNPs
- `BiSnpNM`: combines `BiSnp` and `NM` in a single step
- `EurAF:<maf-threshold>`: filters for `MAF >= maf-threshold`. MAF is determined form the reference data. E.g.: `EurAF:0.01`
- `LD`: prune on LD with the reference defined in `` (`bcftools +prune  -l 0.95 -w 1kb`)
- `QC`: filter on quality (with bcftools: `INFO/MQ>59 & INFO/MQRankSum>-2 & AVG(FORMAT/DP)>20 & AVG(FORMAT/DP)<100 & INFO/QD>15 & INFO/BaseQRankSum>-2 & INFO/SOR<1`)
- `PH`: phase (using beagle) without reference
- `RPH`: phasse (using beagle) with reference defined in `ref_sample` config parameter

IBD/Relatedness steps:

- `GRM`: detect pariwise IBD segments using `germline`
- `FPI`: filter out IBD segments using a mask defined in the reference data.
- `IBD`: estimate pairwise degree of relatedness based on IBD0
- `RVT`: report the estimated degreea vs the true ones

# Datasets
TBP: Add info on datasets (REF and example)

## Reference

### 1000 Genomes EUR (G1K_EUR)

TBP: Add info on datasets (REF and example)

## Examples

### TrueFamily CEU (TFCeu)

TBP: More info on the dataset

# Issues and comments

Please report any issues or ideas at: https://github.com/aehrc/TRIBES/issues

Or contact the *TRIBES* team at: TBP














