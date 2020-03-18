TRIBES
======

[![Documentation Status](https://readthedocs.org/projects/tribes/badge/?version=latest)](http://tribes.readthedocs.io/en/latest/?badge=latest)

This is documentation to TRIBES version 0.2+. For the the documentation for older version 0.1 please check https://github.com/aehrc/TRIBES/tree/branch-0.1 .


*TRIBES* is a user-friendly platform for relatedness detection in genomic data.
*TRIBES* is the first tool which is both accurate (up to 7th degree) and
combines essential data processing steps in a single platform.


We demonstrate the accuracy of *TRIBES* in our publications [here](https://www.biorxiv.org/content/10.1101/686253v1) and [here](https://www.biorxiv.org/content/10.1101/685925v2)

Briefly, input data to *TRIBES* is quality control filtered, joint sample VCF. *TRIBES* then follows these steps:
1) The VCF is filtered using quality metrics contained within the VCF file.  
2) The resultant VCF is then phased using BEAGLE.
3) IBD Segments are then estimated using GERMLINE.
4) Artefactual IBD is masked using a reference file by adjusting segment endpoints.
5) Adjusted IBD Segments are then summed to estimate relationships.
6) *TRIBES* returns result files, including `.csv` of estimated relationships.

To facilitate ease-of-use we employ ‘Snakemake’, a workflow tool which enables flexibility and reproducibility.

The full TRIBES pipeline is described in detail in [Supplementary Material](https://www.biorxiv.org/content/10.1101/686253v1.supplementary-material).

## Learn more
Watch a short video introducing *TRIBES* and its applications
[![TRIBES video](docs/assets/tribes_video.jpg)](https://www.thinkable.org/submission_entries/l3jw6v8G)


See [documentation](https://tribes.readthedocs.io/) for more information on installing and using TRIBES

