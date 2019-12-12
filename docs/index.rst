=======================================
TRIBES
=======================================

**TRIBES** is a user-friendly platform for relatedness detection in genomic data.
**TRIBES** is the first tool which is both accurate (up to 7th degree) and
combines essential data processing steps in a single platform.

Accurately classifying the degree of relatedness between pairs of individuals
has multiple important applications, including disease gene discovery, removal
of confounding relatives in genome wide association studies (GWAS) and family
planning. Currently no tools are available which are accurate beyond 3rd degree
and combine the necessary data processing steps for accuracy and ease of use.
To address this we have developed ‘**TRIBES**’, a user-friendly platform which
leverages the GERMLINE algorithm to accurately identify distant relatives.
**TRIBES** enables user-guided data pruning, phasing of genomes, IBD segment
recovery, masking of artefactual IBD segments and finally relationship
estimation. To facilitate ease-of-use we employ ‘Snakemake’, a workflow tool
which enables flexibility and reproducibility.

We demonstrate the accuracy of **TRIBES** in our publications [here](https://www.biorxiv.org/content/10.1101/686253v1) and [here](https://www.biorxiv.org/content/10.1101/685925v2)

Briefly, input data to **TRIBES** is quality control filtered, joint sample VCF. *TRIBES* then follows these steps:

1. The VCF is filtered using quality metrics contained within the VCF file.  
2. The resultant VCF is then phased using BEAGLE.
3. IBD Segments are then estimated using GERMLINE.
4. Artefactual IBD is masked using a reference file by adjusting segment endpoints.
5. Adjusted IBD Segments are then summed to estimate relationships.
6. **TRIBES** returns result files, including `.csv` of estimated relationships.

The full TRIBES pipeline is described in detail in [Supplementary Material](https://www.biorxiv.org/content/10.1101/686253v1.supplementary-material).



Contents:
---------

.. toctree::
   :maxdepth: 2
   
   getting_started
   
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
