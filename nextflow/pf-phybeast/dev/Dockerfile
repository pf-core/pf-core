FROM frolvlad/alpine-miniconda3

COPY ../../../ /dev/pathfinder

ENV CONDA_DIR="/opt/conda"

# Minimal conda install, see  @ https://jcrist.github.io/conda-docker-tips.html
RUN conda install -c bioconda --yes --no-update-deps \
        lsd \
        goalign \
        raxml-ng \
        fasttree \
        gubbins \
        nomkl \
        pathfinder \
        python=3.7 \
    && pip install /dev/pathfinder
    && conda clean -a \
    && find $CONDA_DIR -follow -type f -name '*.a' -delete \
    && find $CONDA_DIR -follow -type f -name '*.pyc' -delete
