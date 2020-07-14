ARG TAG=3.7
FROM martin37szyska/jupyter-base:$TAG

USER root

WORKDIR $HOME

# Install all OS dependencies for fully functional notebook server
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    emacs-nox \
    vim-tiny \
    git \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    python-dev \
    # ----
    tzdata \
    unzip \
    nano \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Install required packages for minimal datascience and excel support
RUN conda install --quiet --yes \
    'pandas' \
    'openpyxl' \
    'xlrd' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# NB extensions
RUN conda install --quiet --yes \
    'jupyter_contrib_nbextensions' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# copy my nbextensions presets to docker
COPY nbconfig .jupyter/nbconfig

# create startup file for default imports
RUN mkdir -p .ipython/profile_default/startup && \
    fix-permissions .ipython 

COPY startup.py .ipython/profile_default/startup

# create custom css for better visibility
RUN mkdir -p .jupyter && \
    fix-permissions .jupyter

COPY custom .jupyter/custom


# Switch back to martin to avoid accidental container runs as root
USER $NB_USER