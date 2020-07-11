
ARG TAG=3.7.7

FROM martin37szyska/jupyter-base:${TAG}-alpine

USER root

WORKDIR $HOME

# Install required packages for minimal datascience and excel support
RUN conda install --quiet --yes -c conda-forge \
    'pandas' \
    'openpyxl' \
    'xlrd' && \
    conda clean --all -f -y

# NB extensions
RUN conda install --quiet --yes -c conda-forge \
    'jupyter_contrib_nbextensions' && \
    conda clean --all -f -y

# copy my nbextensions presets to docker
COPY nbconfig .jupyter/nbconfig

# create startup file for default imports
RUN mkdir -p .ipython/profile_default/startup && \
    chmod -R 777 .ipython 

COPY startup.py .ipython/profile_default/startup

# create custom css for better visibility
RUN mkdir -p .jupyter && \
    chmod -R 777 .jupyter

RUN mkdir .ipython/profile_default/security && \
    mkdir .ipython/profile_default/log && \
    chmod -R 777 .ipython/profile_default && \
    chmod -R 777 .ipython/profile_default/security && \
    chmod -R 777 .ipython/profile_default/log

COPY custom .jupyter/custom


# Switch back to user to avoid accidental container runs as root
USER  10151