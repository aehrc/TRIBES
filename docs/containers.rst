.. _sec-containers:

===========
Containers
===========

*TRIBES* docker image includes the pipeline and all the dependences and
it's publicly available from https://hub.docker.com/r/piotrszul/tribes
as ``docker.io/piotrszul/tribes`` and the most recent version can pulled
with:

::

    docker pull docker.io/piotrszul/tribes

To use a specifc version e.g.: |version_literal|  please use
|versioned_docker_literal| as the docker image name.

It's an executable image with ``snakemake`` as an entry point.

When running using docker it's necessary to mount the reference data and
pipeline data volumes (or local filesystem) so that the container have
access to both, e.g:

::

    docker -it --rm -v <path-to-ref-data>:<path-to-ref-data> -v <path-to-data>:<path-to-data> docker.io/piotrszul/tribes -d <path-to-data> <other_options> ...

When running with ``singularity`` this may not be need if the volumes
with data and reference data are mounted as per configuration. One
important consideration though is to use ``-e`` flag as some host
environment variables (e.g. related to pyton) casue issues while running
in the containter:

::

    singularity run -e  docker://docker.io/piotrszul/tribes -d <path-to-data> <other_options> ...
