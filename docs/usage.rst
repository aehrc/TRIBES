.. _sec-usage:

=======================================
Usage
=======================================

Read the sections below to run *TRIBES* on your own data, with a custom
pipeline

Input data
----------

*TRIBES* requires the following input files:

-  ``filename.vcf.gz`` - multi-sample VCF file containing sample
   genotypes
-  ``filename.true.rel`` - true pairwise relations (optional, only if a
   user has known relations and wants to calculate accuracy of estimated
   relationships)
-  ``config.yaml`` - pipeline configuration file defining the location
   and name of reference data, the true relations file, the input
   filename and the preprocessing steps required before IBD/relatedness
   estimation

Refer to files inside example dataset ``TFCeu/`` directory for correct
format for these input files.

Preparing a custom pipeline
---------------------------

A key strength of *TRIBES* is that is a flexible pipeline, utilizing
``snakemake``, to enable the user to specify which pre-processing steps
they want to include.

The following steps can used in the pipeline.

Preprocessing:
~~~~~~~~~~~~~~

-  ``NM``: retain only loci with with non-missing genotypes
-  ``BiSnp`` : retain only bi-allelic SNPs
-  ``BiSnpNM``: combines ``BiSnp`` and ``NM`` in a single step
-  ``MAF:<maf-threshold>``: filters for ``MAF >= maf-threshold``, e.g.
   ``MAF:0.01``. MAF is determined from the reference data ``AF``
   annotation which is also added to the output in ``REF_AF``
   annotation.
-  ``LD``: prune on LD with the reference defined in ``G1K_SNP_EUR``
   (``bcftools +prune  -l 0.95 -w 1kb``)
-  ``QC``: filter on quality (with bcftools:
   ``INFO/MQ>59 & INFO/MQRankSum>-2 & AVG(FORMAT/DP)>20 & AVG(FORMAT/DP)<100 & INFO/QD>15 & INFO/BaseQRankSum>-2 & INFO/SOR<1``)
-  ``PH``: phase (using beagle) without reference
-  ``RPH``: phase (using beagle) with reference defined in
   ``ref_sample`` config parameter

IBD/Relatedness steps:
~~~~~~~~~~~~~~~~~~~~~~

-  ``GRM``: detect pariwise IBD segments using ``germline``
-  ``FPI``: filter out IBD segments using a mask defined in the
   reference data.
-  ``IBD``: estimate pairwise degree of relatedness based on IBD0
-  ``RVT``: compare the estimated degree to the known degree, reflecting
   accuracy

Examples
--------

Example 1
~~~~~~~~~

For example, a user may wish to identify relationships using an unphased
input VCF. They wish to filter on allele frequency of MAF = 0.01 and
then phase the data using reference file and estimate relatedness. They
would then need to edit the ``config.yaml`` file from the example data
``TFCeu`` directory to reflect their input VCF filename and processing
steps. Their input VCF file should be in the same ``TFCeu`` directory,
for the ``config.yaml`` file to work.

Their ``config.yaml`` file would look like this:

-  rel\_sample: ``filename_BiSnpNM_MAF:0.01_RPH`` [where ``filename``
   refers to the input VCF filename]
-  ref\_dir: ``../REF_G1K-EUR_0.001`` [where ref\_dir is the location of
   the reference directory, which hosts the cohost used for filtering on
   MAF and LD, phasing and masking steps]

The user would then run *TRIBES* from the installation directory as in
the `Getting started <#Getting-started>`__ section

::

    ./tribes -d $HOME/tribes-data/TFCeu -j <no_cpu_cores> estimate_degree

where\ ``estimate_degree`` is an alias which calls *TRIBES* to perform
the ``GRM``, ``FPI`` and ``IBD`` steps described under 'IBD/Relatedness
steps' in `Preparing a custom pipeline <#Preparing-a-custom-pipeline>`__

Example 2
~~~~~~~~~

Alternatively, a user may want to identify novel relationship, as well
as confirm known relationships. They wish to pre-process the VCF to
filter on MAF = 0.01 and quality metrics, then phase the data using
reference, estimate relationships and compare estimated with known
relationships.

Their ``config.yaml`` file would look like this:

-  rel\_sample: ``filename_BiSnpNM_MAF:0.01_QC_RPH``
-  ref\_dir: ``../REF_G1K-EUR_0.001``
-  rel\_true: ``filename.true.rel`` [a reference file containing known
   relationships,required if step ``RVT`` is used in the pipeline]

The user would then run *TRIBES* from the installation directory as in
the `Getting started <#Getting-started>`__ section

::

    ./tribes -d $HOME/tribes-data/TFCeu -j <no_cpu_cores> estimate_degree_vs_true

If users provide a ``rel_true:`` file in the ``config_yaml`` file, they
can call ``estimate_degree_vs_true`` which is an alias that calls
*TRIBES* to perform the ``GRM``, ``FPI``, ``IBD`` and ``RVT`` steps
described under 'IBD/Relatedness steps' in `Preparing a custom
pipeline <#Preparing-a-custom-pipeline>`__
