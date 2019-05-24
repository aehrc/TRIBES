Info on how to build and deploy (ana)conda packages
===================================================

## Building the packages

Create a new conda environemt (e.g. `conda-build`) and activate.

Install `conda-build` and `anaconda-client`

	conda install  -y conda-build anaconda-client

Build a package (e.g. `gemline`)

	conda-build germline

Write down the path the package (e.g.: `/Users/szu004/miniconda2/envs/conda-build/conda-bld/osx-64/germline-1.5.3-0.tar.bz2`)

Build packages for other platforms (e.g. `osx-64`, `linux-64`, `linux-32`):

	conda convert --platform linux-64 /Users/szu004/miniconda2/envs/conda-build/conda-bld/osx-64/germline-1.5.3-0.tar.bz2

Login to anaconda( username is aerhc):

	anaconda login

Upload the package:

	anaconda upload /Users/szu004/miniconda2/envs/conda-build/conda-bld/osx-64/germline-1.5.3-0.tar.bz2


## More info

Complete documentation at: https://docs.conda.io/projects/conda-build/en/latest/index.html
