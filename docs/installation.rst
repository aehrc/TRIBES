.. _sec-installation:

=======================================
Installation
=======================================

Installation for workstation use
--------------------------------

*TRIBES* requires a 64-bit version of Linux, MacOS or Windows 10.

Windows Subsystem for Linux (WSL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run *TRIBES* on Windows 10, first install
`Ubuntu <https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6>`__ from
the Microsoft Store.

Then open the Ubuntu app from the Start menu.

Miniconda
~~~~~~~~~

*TRIBES* has a list of dependencies required to be installed prior to
running the analysis pipeline. For this, we use
`Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__.

Install ``miniconda`` (3.7 or 2.7) from
https://docs.conda.io/en/latest/miniconda.html:

::

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh Miniconda3-latest-Linux-x86_64.sh

Download *TRIBES*
~~~~~~~~~~~~~~~~~

Download the latest release of *TRIBES* from
https://github.com/aehrc/TRIBES/releases and extract it to your selected
directory.

Alternatively you can clone the most recent (unstable) version from
github:

::

    git clone https://github.com/aehrc/TRIBES.git

Installing *TRIBES*
~~~~~~~~~~~~~~~~~~~

Go to the *TRIBES* installation directory.

Install dependencies (requires about 500 MB for software packages):

::

    ./setup/install-with-conda.sh

This will create an conda environment named ``tribes`` and install all
required dependencies, as well as create the appropriate *TRIBES*
configuration file at ``~/.tribesrc``

To check the installation run:

::

    ./tribes

This should display among others usage info.

After you install *TRIBES*, return to :ref:`subsec-getting_started-testing_installation_on_example_dataset` 
to test the installation on example data.

Manual installation
-------------------

*TRIBES* is implemented as a ``snakemake`` pipeline and relies a number
of bioinformatics tools for processing, such as ``bcftools``, ``bgzip``,
``tabix``, ``vcftools``, ``germline``, ``beagle`` as well as a number of
``python`` an ``R`` packages.

The complete list of dependencies and their required (minimal) versions
can be inferred from the conda environment file at:
`setup/environment.yaml <setup/environment.yaml>`__

They can be installed using the OS specific way (e.g. using ``apt`` or
``yum`` on Linxu or ``brew`` on MacOS)

In addition *TRIBES* requires ``tribes.tools`` ``R`` packages which can
be installed from sources with:

::

    Rscript --vanilla -e "install.packages('R/tribes.tools',repos=NULL)"

Installation on HPC Cluster
---------------------------

``snakemake`` and thus *TRIBES* can run on HPC clusters (for example
with ``slurm``).

An example setup for CSIRO HPC cluster is descibed in
`README-CSIRO.md <README-CSIRO.md>`__ and can be used as a guide to
configure *TRIBES* on other clusters.

For more information on running ``snakemake`` on HPC clusters please
check the ``snakemake`` documentation
https://snakemake.readthedocs.io/en/stable/
