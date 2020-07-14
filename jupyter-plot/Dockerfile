ARG TAG=3.7

FROM martin37szyska/jupyter-minimal:$TAG

ARG CURRENTUSER=$NB_USER
USER root

WORKDIR $HOME

# install matplotlib 
RUN conda install --quiet --yes \
    'matplotlib' \
    'seaborn' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# extend startup config with startup.ext
COPY startup.ext .ipython/profile_default/startup

WORKDIR ${HOME}/.ipython/profile_default/startup

RUN cat startup.ext >> startup.py && \
    rm startup.ext

# Switch back to martin to avoid accidental container runs as root
USER $CURRENTUSER

WORKDIR $HOME