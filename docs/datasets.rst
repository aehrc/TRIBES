.. _sec-datasets:

========
Datasets
========

1000 Genomes EUR (REF\_G1K-EUR\_0.001)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Location:
https://d3o0p4nu4e38rq.cloudfront.net/downloads/reference/1.0/REF_G1K-EUR_0.001.tar.gz

This is a reference dataset used for MAF filtering, LD pruning and
phasing. It's based on the data from release 3 of `1000 Genomes
Project <http://www.internationalgenome.org/>`__. It includes all
biallelic SNPs with ``MAF > 0.001`` for unrelated invidiuals from 'EUR'
superpopulation.

-  ``VCF`` : all sample genotypes (separate file per chromosome)
-  ``sample.txt`` : list of included EUR samples
-  ``ersa-mask.tsv``: list of regions with excessive IBD (generated with
   `ersa <http://www.hufflab.org/software/ersa/>`__ for this sample)
-  ``plink.chrALL.GRCh37.map.gz``: genetic map (included for
   convenience)

TrueFamily CEU (TFCeu)
~~~~~~~~~~~~~~~~~~~~~~

Location:
https://d3o0p4nu4e38rq.cloudfront.net/downloads/examples/0.2/TFCeu.tar.gz

This is synthetic dataset with simulated genotypes based on unrelated
individuals from CEU population of `1000 Genomes
Project <http://www.internationalgenome.org/>`__. The pedigree is
defined in ``g1k_ceu_family_15_2.ped`` and includes 15 generations.

-  ``TF-CEU-15-2.vcf.gz`` : VFC file for the simulated genotypes
-  ``g1k_ceu_family_15_2.ped``: pedigree
-  ``TF-CEU-15-2.true.rel`` : true relations
