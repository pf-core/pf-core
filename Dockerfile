FROM frolvlad/alpine-miniconda3

ENV CONDA_DIR="/opt/conda"

# Minimal conda install, see  @ https://jcrist.github.io/conda-docker-tips.html
RUN conda install -c bioconda --yes --no-update-deps \
        wget \
        tqdm \
        colorama \
        pandas \
        click \
        pytest \
        seaborn \
        scipy \
        python-dateutil \
        numpy \
        pymongo \
        flask \
        paramiko \
        flask-socketio \
        flask-cors \
        mongodb \
        pysam \
        nextflow\
        nomkl \
        python=3.7 \
    && pip install mongoengine \
    && conda clean -a \
    && find $CONDA_DIR -follow -type f -name '*.a' -delete \
    && find $CONDA_DIR -follow -type f -name '*.pyc' -delete
