FROM continuumio/miniconda

ENV CONDA_DIR="/opt/conda"

# LSD2 compiler
RUN apt-get install g++ make --yes \
    && mkdir /src \
    && cd /src \
    && git clone https://github.com/tothuhien/lsd2.git \
    && cd /src/lsd2/src \
    && make \
    && ln -s /src/lsd2/src/lsd2 /bin/lsd2

# Minimal conda install, see  @ https://jcrist.github.io/conda-docker-tips.html
RUN conda install -c bioconda -c genomedk --yes --no-update-deps \
        nextflow \
        goalign \
        trimmomatic \
        raxml-ng \
        fasttree \
        treetime \
        gubbins \
        pysam \
        nomkl \
        python=3.7

# Snippy install with specific channels for v4
RUN conda install -c conda-forge -c bioconda -c defaults snippy

# Cleanup
RUN conda clean -a \
    && find $CONDA_DIR -follow -type f -name '*.a' -delete \
    && find $CONDA_DIR -follow -type f -name '*.pyc' -delete

