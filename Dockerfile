FROM continuumio/miniconda3:latest

#  $ docker build . -t aehrc/tribes
#  $ docker run --rm -it aehrc/tribes -d <workdir>
#  $ docker push aehrc/tribes
MAINTAINER Piotr Szul <Piotr.Szul@data61.csiro.au>

# Resolve issue with undefined user name for LDAP users, e.g remove warnings
#  group..
#  username..
RUN apt-get update && \
 apt-get upgrade -y && \
 apt-get install -y --no-install-recommends libnss-sss

# Solve locale issues when running bash.
#   /bin/bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
#
# It breaks conda version check in snakemake:
RUN apt-get clean && apt-get update && apt-get install -y locales && \
    echo "LC_ALL=en_US.UTF-8" >> /etc/environment  && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen  && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf  && \
    locale-gen en_US.UTF-8

# JAVA 8 missing fonts workaround:
# see https://bugs.debian.org/793210
# and https://github.com/docker-library/java/issues/46#issuecomment-119026586
# P.S: our java comes from conda, seems the same issue
RUN apt-get install -y --no-install-recommends libfontconfig1

# Install additional tools: ps, htop, vim
RUN apt-get install -y procps htop vim

# Cleanup
RUN rm -rf /var/lib/apt/lists/*

# Install snakemake and other packages
COPY setup/environment.yaml /root/environment.yaml
RUN conda update  --yes -n base -c defaults conda && \
    conda env update -n base --file /root/environment.yaml && \
    conda clean   --yes --all
RUN rm /root/environment.yaml


#Install package
COPY R /root/R
RUN Rscript --vanilla -e "install.packages('/root/R/tribes.tools',repos=NULL)"
RUN rm -rf /root/R

#Install package
COPY Snakefile config.yaml *.smake /opt/tribes/
COPY scripts /opt/tribes/scripts
COPY python /opt/tribes/python
COPY notebooks /opt/tribes/notebooks
ENV PATH=$PATH:/opt/tribes/scripts
ENTRYPOINT ["snakemake","-s","/opt/tribes/Snakefile"]
