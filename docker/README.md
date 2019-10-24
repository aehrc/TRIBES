

Based on: https://github.com/JetBrains-Research/docker-images/tree/master/biolabs/snakemake


To build:

	docker build -t aehrc/tribes .

How to mount local directories:

	docker run -it -v `pwd`:/workdir -w /workdir aehrc/tribes snakemake TF-CEU_BiSnp/chr21.vcf.gz